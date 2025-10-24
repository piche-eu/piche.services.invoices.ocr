import os
import pytesseract
from PIL import Image
from proxy import client
from pathlib import Path
import gradio as gr
from ollama_ocr import OCRProcessor
from docling.document_converter import DocumentConverter
from paddleocr import PaddleOCR

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

def parse_with_llava(filepath, model="granite3.2-vision:2b"):
    ocr = OCRProcessor(model_name=model)
    result = ocr.process_image(
        image_path=filepath,
        forfilepathmat_type="text",
        custom_prompt="Extract all text and provide it as an output <Text>, Please provide the output tables <Table> as json with exact values . Please extact all the text fields and values associated with that fields.",
    )
    return None, None  # result, filepath

def upload_file(filepath):
    # Transfer the file to the grpc server
    path = os.path.dirname(filepath)
    name = Path(filepath).name
    if dropdown.value == "granite":
        response = parse_with_llava(path + "/" + name)
    elif dropdown.value == "docling":
        response = parse_with_docling(path + "/" + name)
    elif dropdown.value == "moondream:1.8b":
        response = parse_with_llava(path + "/" + name, model="moondream:1.8b")
    elif dropdown.value == "paddle":
        response, filepath = parse_with_paddle(filepath)
    elif dropdown.value == "gRPC":
        _client = client.Client()
        _client.send_file(filepath)
    return response, filepath

def download_file():
    return [gr.UploadButton(visible=True), gr.DownloadButton(visible=False)]

with gr.Blocks() as demo:
    gr.Markdown(
        "First upload a file and and then you'll be able download it (but only once!)"
    )
    with gr.Row():
        dropdown = gr.Dropdown(
            [
                "gRPC",
                "llava",
                "docling",
                "tesseract",
                "paddle",
                "granite3.2-vision:2b",
                "moondream:1.8b",
            ],
            label="OCR",
            interactive=True,
            info="OCR Engine",
        )
    # with gr.Row():
    #     api = gr.Interface(
    #         fn=None,
    #         inputs=gr.Textbox(
    #             lines=5, placeholder="localhost:50051", label="Input Text"
    #         ),
    #         outputs="textbox",
    #     )
    # with gr.Row():
    #     server_address = gr.Interface(
    #         fn=None,
    #         inputs=gr.Textbox(
    #             lines=5, placeholder="localhost:50051", label="Input Text"
    #         ),
    #         outputs="textbox",
    #     )
    with gr.Row():
        upload_button = gr.UploadButton("Upload a file", file_count="single")
    with gr.Row():
        t = gr.Textbox()
    with gr.Row():
        pdf_viewer = gr.Image(label="PDF Viewer")
    dropdown.change(fn=rs_change, inputs=[dropdown], outputs=[dropdown])
    upload_button.upload(upload_file, upload_button, [t, pdf_viewer])

if __name__ == "__main__":
    demo.launch()
