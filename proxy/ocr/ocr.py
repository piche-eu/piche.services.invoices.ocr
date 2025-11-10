import os
import base64
import pymupdf
from PIL import Image
from mistralai import Mistral
from docling.document_converter import DocumentConverter
from rich.markdown import Markdown
from rich.console import Console
from dotenv import load_dotenv

load_dotenv()
console = Console()


class OCREngine:
    def __init__(self, config=None):
        """_summary_

        :param config: _description_, defaults to None
        :type config: _type_, optional
        """
        self.config = config

    def pdf2base64(self, filepath):
        try:
            with open(filepath, "rb") as pdf_file:
                return base64.b64encode(pdf_file.read()).decode("utf-8")
        except FileNotFoundError:
            print(f"Error: The file {filepath} was not found.")
            return None
        except Exception as e:  # Added general exception handling
            print(f"Error: {e}")
            return None

    def mistral_ocr(self, base64_pdf, api_key: str = ""):
        # Extract from env-variable
        try:
            api_key = os.environ["MISTRAL_API"]
        except Exception as e:
            print("No API KEY MISTRAL_API")
            raise e
        else:
            client = Mistral(api_key=api_key)
            ocr_response = client.ocr.process(
                model="mistral-ocr-latest",
                document={
                    "type": "document_url",
                    "document_url": f"data:application/pdf;base64,{base64_pdf}",
                },
                include_image_base64=True,
            )
            return ocr_response

    def pdf2im(self, filepath: str):
        image_path: list[str] = []
        dir_name: str = os.path.dirname(filepath)
        with pymupdf.open(filepath) as doc:
            for idx in range(doc.page_count):
                pix = doc[idx].get_pixmap()
                temp_path = f"{filepath}_page_{idx}.png"
                pix.save(temp_path)
                image_path.append(temp_path)
        return image_path[0]

    def bytes2bytes64(self, bytes):
        return base64.b64encode(bytes).decode("utf-8")

    def process_file(self, filepath: str):
        # convert the file to desired format
        image_path = self.pdf2im(filepath)
        return image_path

    def im2text(self, image):
        # Currently suspended not works well;
        # # call the OCR
        # ocr = PaddleOCR(
        #      use_doc_orientation_classify=False,
        #      use_doc_unwarping=False,
        #      use_textline_orientation=False,
        #  )

        # paddle_result = ocr.predict(input=f"{image}")
        # # post_process_paddle
        # paddle_text = ["".join([text[0][0] for text in lin]) for lin in paddle_result]
        # tesseract
        # tesseract_result = pytesseract.image_to_data(
        #     Image.open(image), output_type="data.frame"
        # )
        # tesseract_text = tesseract_result["text"][
        #     (tesseract_result["text"].isna() == False)
        # ].to_list()
        # post process the results
        # return paddle_text, tesseract_text
        return

    def doc2text(self, filepath: str, verbose: bool = 1):
        converter = DocumentConverter()
        doc = converter.convert(filepath).document
        markdown = doc.export_to_markdown()
        if verbose:
            md = Markdown(markdown)
            console.print(md)
        return md

    def agentic_parser(self, prompt: str) -> str:
        return

    def run_text_hrm(self, prompt: str) -> str:
        return
