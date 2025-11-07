import os
import sys
sys.path.append(".")
import grpc
sys.path.append("/usr/app/grpc_compiled/")
import file_service_pb2
import file_service_pb2_grpc
from concurrent import futures
import logging
#from dotenv import load_dotenv, find_dotenv
#load_dotenv(find_dotenv())
logger = logging.getLogger(__name__)
from ocr import ocr
from ocr import ocr_llm
import pandas as pd
import json

__all__ = "FileServer"

SERVER_ADDRESS = "0.0.0.0:50051"
SERVER_ID = 1
import multiprocessing
multiprocessing.set_start_method("spawn", force=True)

class FileServiceServicer(file_service_pb2_grpc.FileServiceServicer):
    
    def __init__(self):
        super().__init__()
        llm_config = ocr_llm.LLMConfig
        self.llm = ocr_llm.OCRLLM(llm_config)
    
    def UploadFile(self, request_iterator, context):
        """Server-side implementation for the client-streaming UploadFile RPC."""
        filename = None
        file_size = 0
        file_path = "uploads/"  # Directory to save files
        # 1. Ensure upload directory exists
        os.makedirs(file_path, exist_ok=True)
        # based on the config stage process this file and extract ocr;
        # 2. Iterate through the stream of incoming messages
        for request in request_iterator:
            # First message must contain the filename
            if request.HasField("filename"):
                if filename is not None:
                    # Should not receive filename after the first chunk
                    context.abort(
                        grpc.StatusCode.INVALID_ARGUMENT,
                        "Metadata received multiple times",
                    )

                filename = request.filename
                print(f"Starting upload for file: {filename}")
                file_handle = open(os.path.join(file_path, filename), "wb")

            # Process the file using ocr
            # retrieve the name of the service -> for example ocr_service = "MISTRAL_OCR"
            # retrieve the API key ->

            # Subsequent messages contain file chunks
            elif request.HasField("chunk_data"):
                if filename is None:
                    # Chunks should not arrive before metadata
                    context.abort(
                        grpc.StatusCode.FAILED_PRECONDITION,
                        "File metadata not received",
                    )

                chunk = request.chunk_data
                file_handle.write(chunk)
                file_size += len(chunk)
            else:
                context.abort(
                    grpc.StatusCode.INVALID_ARGUMENT, "Request has no data field."
                )
        ocr_engine = ocr.OCREngine()
        bytes64 = ocr_engine.bytes2bytes64(chunk)
        try:
            response = ocr_engine.mistral_ocr(bytes64)
            mistral_result = response.pages[0].markdown
            
            #im_path = ocr_engine.process_file("./" + file_path + "/" + filename)
            #paddle_ocr, tesseract = ocr_engine.im2text(im_path)
            #print("Mistral Result: ", paddle_ocr, tesseract )
        except Exception as e:
            print(f"!Exception: {e}")
        finally:
            # print("Run the LLM for the text extraction:")
            llm_response = self.llm.extract_text(mistral_result)
            df = pd.DataFrame.from_dict(llm_response, orient='index')
            df.columns = ['values']
            df = df.iloc[1:]
            md = df.to_markdown()
        # 3. Close the file and return the final response
        if filename and file_handle:
            file_handle.close()
            print(f"Finished upload. Saved {filename} ({file_size} bytes)")
            return file_service_pb2.FileUploadResponse(message=f"{md}", size=file_size)
        else:
            context.abort(grpc.StatusCode.ABORTED, "No file data received.")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    file_service_pb2_grpc.add_FileServiceServicer_to_server(
        FileServiceServicer(), server
    )
    server.add_insecure_port(SERVER_ADDRESS)
    print("------------------start Python GRPC server")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
