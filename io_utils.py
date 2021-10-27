import io
import gzip


io_buffer = io.BytesIO()
io_buffer.seek(0)
compressed_bytes = gzip.compress(io_buffer.read())
