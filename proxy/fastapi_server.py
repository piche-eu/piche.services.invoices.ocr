import os
import sys

sys.path.append(".")
from concurrent import futures
import base64
from pydantic import BaseModel
from ocr import ocr
from ocr import ocr_llm
import pandas as pd
import json
from fastapi import FastAPI, UploadFile, File
import shutil

# logger = logging.getLogger(__name__)

__all__ = "FileServer"

SERVER_ADDRESS = "0.0.0.0:50051"
SERVER_ID = 1
import multiprocessing

multiprocessing.set_start_method("spawn", force=True)


app = FastAPI()
llm_config = ocr_llm.LLMConfig
llm = ocr_llm.OCRLLM(llm_config)
ocr_engine = ocr.OCREngine()


class Data(BaseModel):
    filename: str
    data: str | None = None


@app.post("/upload-base64-file/")
async def upload_base64_file(data: Data):
    print(type(data.data))
    try:
        # Decode the base64 string
        img_recovered_bytes = base64.b64decode(data.data)

        # Define the path to save the file
        save_path = os.path.join("uploaded_files", data.filename)
        print(save_path)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Save the decoded content to a file
        with open(save_path, "wb") as f:
            f.write(img_recovered_bytes)
    except Exception as e:
        return {"message": f"Error uploading file: {e}"}
    try:
        response = ocr_engine.mistral_ocr(data.data)
        mistral_result = response.pages[0].markdown
    except Exception as e:
        print(f"!Exception: {e}")
        return {"message": f"Error uploading file: {e}"}
    try:
        print("Run the LLM for the text extraction:")
        llm_response = llm.extract_text(mistral_result)
        df = pd.DataFrame.from_dict(llm_response, orient="index")
        df.columns = ["values"]
        df = df.iloc[1:]
        md = df.to_markdown()
        print("llm_response:", llm_response)
        return {"message": f"File '{md}' uploaded successfully."}
    except Exception as e:
        return {"message": f"Error uploading file: {e}"}
