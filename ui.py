import os
from pathlib import Path

import gradio as gr
# from ollama_ocr import OCRProcessor
import pytesseract
from docling.document_converter import DocumentConverter
from paddleocr import PaddleOCR
from PIL import Image

global dropdown_val


def rs_change(choise):
    dropdown.value = choise
    return choise


def parse_with_docling(filepath):
    converter = DocumentConverter()
    doc = converter.convert(filepath).document
    return doc.export_to_markdown()


def parse_with_tesseract(filepath):
    parsed_file = pytesseract.image_to_data(
        Image.open(filepath), output_type="data.frame"
    )
    return parsed_file


def parse_with_paddle(filepath):
    ocr = PaddleOCR(
        use_doc_orientation_classify=True,
        use_doc_unwarping=True,
        use_textline_orientation=True,
    )
    result = ocr.predict(input=f"{filepath}")
    text = [line for line in result[0]["rec_texts"]]
    result[0].save_to_img("./png/" + "output")
    im_path = (
        os.path.dirname(filepath) + "/png/output" + os.path.basename(filepath) + ".png"
    )
    return text, im_path


def parse_with_llava(filepath, model="llava:latest"):
    # ocr = OCRProcessor(model_name='llava:latest')
    # result = ocr.process_image(
    #    image_path=filepath,
    #    format_type="text",
    #    custom_prompt="Extract all text and provide it as an output <Text>, Please provide the output tables <Table> as json with exact values . Please extact all the text fields and values associated with that fields."
    # )
    return None, None  # result, filepath


def upload_file(filepath):
    path = os.path.dirname(filepath)
    name = Path(filepath).name
    if dropdown.value == "llava":
        response = parse_with_llava(path + "/" + name)
    elif dropdown.value == "docling":
        response = parse_with_docling(path + "/" + name)
    elif dropdown.value == "gemma":
        response = parse_with_llava(path + "/" + name, model="gemma3:latest")
    elif dropdown.value == "paddle":
        response, filepath = parse_with_paddle(filepath)
    return response, filepath


def download_file():
    return [gr.UploadButton(visible=True), gr.DownloadButton(visible=False)]


with gr.Blocks() as demo:
    gr.Markdown(
        "First upload a file and and then you'll be able download it (but only once!)"
    )
    with gr.Row():
        dropdown = gr.Dropdown(
            ["llava", "docling", "tesseract", "paddle", "granite", "gemma"],
            label="OCR",
            interactive=True,
            info="OCR Engine",
        )
    with gr.Row():
        upload_button = gr.UploadButton("Upload a file", file_count="single")
    with gr.Row():
        t = gr.Textbox()
    with gr.Row():
        pdf_viewer = gr.Image(label="PDF Viewer")
    dropdown.change(fn=rs_change, inputs=[dropdown], outputs=[dropdown])
    upload_button.upload(upload_file, upload_button, [t, pdf_viewer])


if __name__ == "__main__":
    demo.launch(share=True)
