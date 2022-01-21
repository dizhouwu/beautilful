from git import Repo, Git, GitCommandError
import os
import tempfile

SSH_REPO_PATH = ""
TMP_DIR = "/tmp"
SSH_KEY_FILE_NAME = "id_rsa"


with tempfile.TemporaryDirectory(dir=TMP_DIR) as tmpdirname:
    ssh_work_dir = os.path.join(work_dir, "ssh")
    git_work_dir = os.path.join(work_dir, "git")
    ssh_key_file_dir = os.path.dirname(os.path.abspath(__file__))
    ssh_key_file_dir = os.path.join(ssh_key_file_dir, "ssh")
    if not os.path.isdir(ssh_key_file_dir):
        raise RuntimeError("Can't find SSH key files..")

    shutil.copytree(ssh_key_file_dir, ssh_work_dir)
    ssh_key_file_dir = os.path.join(ssh_work_dir, SSH_KEY_FILE_NAME)
    os.chmod(ssh_key_file_dir, 0o400)

    git_ssh_identity_file = ssh_key_file_dir
    git_ssh_cmd = f"ssh -i {git_ssh_identity_file}"

    local_repo = Repo.clone_from(
        SSH_REPO_PATH,
        git_work_dir,
        branch="master",
        env={"GIT_SSH_COMMAND": git_ssh_cmd},
    )

    commit_message = f"Some random msg"
    local_repo.git.add(all=True)

    try:
        local_repo.git.commit("-m", commit_message)
        local_repo.git.push("--set-upstream", local_repo.remote().name, "master")
    except GitCommandError as e:
        logger.error(str(e))

    logger.info("Done")
