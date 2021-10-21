from typing import List, Dict
from azure.storage.blob import ContainerClient

class AzureBlobSyncClient:
    def __init__(self, connect_str: str, container_name: str):
        self.container_client = ContainerClient.from_connection_string(
            conn_str=connect_str,
            container_name=container_name,
        )
        self.container_name = container_name

    def _create_container(self):
        self.container_client.create_container()

    def _list_blobs(self):
        return self.container_client.list_blobs()

    def _delete_blobs(self):
        for blob in self._list_blobs():
            self.container_client.delete_blob(blob)

    def _delete_container(self):
        self.container_client.delete_container()

    def post_file_to_azure_blob(self, input_file_path, blob_path):
        with open(input_file_path, "rb") as f:
            self.container_client.upload_blob(name=blob_path, data=f)

    def post_files_to_azure_blob(self, input_file_paths: List[str], blob_paths: List[str]):
        for input_file_path, blob_path in zip(input_file_paths, blob_paths):
            self.post_file_to_azure_blob(input_file_path, blob_path)

    def post_bytes_to_azure_blob(self, bytes_data: bytes, blob_path: str):
        self.container_client.upload_blob(name=blob_path, data=bytes_data)

    def post_list_of_bytes_to_azure_blob(self, bytes_list: List[bytes], blob_paths: List[str]):
        for bytes_data, blob_path in zip(bytes_list, blob_paths):
            self.post_bytes_to_azure_blob(bytes_data, blob_path)
