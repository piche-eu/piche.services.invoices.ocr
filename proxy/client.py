import grpc
import file_service_pb2
import file_service_pb2_grpc
import os

# Define the size of each chunk
CHUNK_SIZE = 1024 * 1024  # 1MB


class Client:
    def __init__(self):
        return

    def upload_file(self,stub, file_to_upload):
        """Calls the client-streaming RPC."""
        print("Start file transfer")
        try:
            # Create a generator for the requests
            requests = file_chunk_generator(file_to_upload)

            # Call the RPC and pass the generator
            response = stub.UploadFile(requests)

            print("\n--- gRPC Response ---")
            print(f"Status: {response.message}")
            print(f"Size Received: {response.size} bytes")

        except grpc.RpcError as e:
            print(f"An error occurred: {e.details()}")
        return

    def __call__(self, *args, **kwds):
        return


def file_chunk_generator(file_path):
    """A generator to yield FileUploadRequest messages."""

    # 1. Send the file metadata (filename) first
    filename = os.path.basename(file_path)
    yield file_service_pb2.FileUploadRequest(filename=filename)

    # 2. Stream the file in chunks
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            # Yield a message with the chunk data
            yield file_service_pb2.FileUploadRequest(chunk_data=chunk)


def send_configuration(stub, config):
    try:
        response = stub.SendConfig(config)
        print("\n--- gRPC Response ---")
        print(f"Status: {response.message}")
        print(f"Size Received: {response.size} bytes")

    except grpc.RpcError as e:
        print(f"An error occurred: {e.details()}")

    return


# --- Client Execution ---
if __name__ == "__main__":
    # Use a secure channel for production; insecure for testing
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = file_service_pb2_grpc.FileServiceStub(channel)
        filepath = "TODO ADD THE FILEPATH HERE"
        client = Client()
        client.upload_file(stub, filepath)
