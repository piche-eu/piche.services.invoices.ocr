import os
import sys

sys.path.append(".")
import json
import shutil
import base64
from ocr import ocr
import pandas as pd
from ocr import ocr_llm
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File
from logger import logger
from concurrent import futures
import multiprocessing

multiprocessing.set_start_method("spawn", force=True)

__all__ = "FileServer"
SERVER_ADDRESS = "0.0.0.0:50051"
SERVER_ID = 1


app = FastAPI()
llm_config = ocr_llm.LLMConfig
llm = ocr_llm.OCRLLM(llm_config)
ocr_engine = ocr.OCREngine()


class Data(BaseModel):
    filename: str
    data: str | None = None


@app.post("/upload-base64-file/")
async def upload_base64_file(data: Data):
    try:
        # Decode the base64 string
        filename = data.filename
        logger.info("message={}".format("Received the file:" + filename))
        img_recovered_bytes = base64.b64decode(data.data)
        # Define the path to save the file
        save_path = os.path.join("uploaded_files", data.filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        # Save the decoded content to a file
        with open(save_path, "wb") as f:
            f.write(img_recovered_bytes)
        logger.info(
            "message={}".format("Decoded and saved the file: " + str(save_path))
        )

    except Exception as e:
        logger.critical(
            "message={}".format("An unhandled critical error:" + str(e), exc_info=True)
        )
        return {"message": f"Error uploading file: {e}"}
    try:
        response = ocr_engine.mistral_ocr(data.data)
        mistral_result = response.pages[0].markdown
    except Exception as e:
        print(f"!Exception: {e}")
        logger.critical(
            "message={}".format("An unhandled critical error:" + str(e)), exc_info=True
        )
        return {"message": f"Error uploading file: {e}"}
    try:
        logger.info("Run the Ollama LLM for the text extraction:")
        llm_response = llm.extract_text(mistral_result)
        df = pd.DataFrame.from_dict(llm_response, orient="index")
        df.columns = ["values"]
        df = df.iloc[1:]
        md = df.to_markdown()
        logger.info(
            "message={}".format(
                "Run the LLM for the text extraction:" + str(llm_response)
            )
        )
        return {"message": f"File '{md}' uploaded successfully."}
    except Exception as e:
        logger.critical(
            "message={}".format("An unhandled critical error:" + str(e)), exc_info=True
        )
        return {"message": f"Error uploading file: {e}"}
