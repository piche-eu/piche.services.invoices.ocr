import os
import pymupdf
import argparse
import pytesseract
from PIL import Image
from paddleocr import PaddleOCR
from docling.document_converter import DocumentConverter


def pdf2im(filepath):
    image_path = []
    dir_name = os.path.dirname(filepath)
    with pymupdf.open(filepath) as doc:
        for idx in range(doc.page_count):
            pix = doc[idx].get_pixmap()
            temp_path = f"{filepath}_page_{idx}.png"
            pix.save(temp_path)
            image_path.append(temp_path)
    return image_path


def process_file(filepath):
    # convert the file to desired format
    image_path = pdf2im(filepath)
    return image_path


def im2text(image):
    # call the OCR
    ocr = PaddleOCR(
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
    )

    paddle_result = ocr.predict(input=f"{image}")
    # post_process_paddle
    paddle_text = [text[0][0] for text in lin for lin in paddle_result]

    # tesseract
    tesseract_result = pytesseract.image_to_data(
        Image.open(image), output_type="data.frame"
    )
    tesseract_text = tesseract_result["text"][
        (tesseract_result["text"].isna() == False)
    ].to_list()
    # post process the results
    return paddle_text, tesseract_text


def doc2text(filepath):
    converter = DocumentConverter()
    doc = converter.convert(filepath).document
    return doc.export_to_markdown()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-file", type=str, default=None, 
                        help="image file")
    args = parser.parse_args()
    result = doc2text(args.image_file)
    print(result)
    