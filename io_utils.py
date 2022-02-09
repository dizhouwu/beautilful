import io
import gzip


io_buffer = io.BytesIO()
io_buffer.seek(0)
compressed_bytes = gzip.compress(io_buffer.read())

with gzip.open(gz_file_path, mode="wb") as f_out:
    shutil.copyfileobj(f, f_out)  # copyfileobj will perform chunking by default
