import os

import pdb
import base64
import pymupdf
import argparse
import pytesseract
from PIL import Image
from mistralai import Mistral
from paddleocr import PaddleOCR
from docling.document_converter import DocumentConverter
from rich.markdown import Markdown
from rich.console import Console
from io import BytesIO
import json
import psutil
import subprocess
console = Console()

class OCREngine():
    def __init__(self, config=None):
        """_summary_

        :param config: _description_, defaults to None
        :type config: _type_, optional
        """
        self.config = config
    
    def pdf2base64(self, filepath):
        try:
            with open(filepath, "rb") as pdf_file:
                return base64.b64encode(pdf_file.read()).decode('utf-8')
        except FileNotFoundError:
            print(f"Error: The file {filepath} was not found.")
            return None
        except Exception as e:  # Added general exception handling
            print(f"Error: {e}")
            return None

    def mistral_ocr(self, base64_pdf, api_key:str=""):
        #Extract from env-variable
        api_key = "cvdIgzhzTk6S5iWB6CctYwtrRucFIYoq"
        #os.environ["MISTRAL_API"]
        client = Mistral(api_key=api_key)
        ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": f"data:application/pdf;base64,{base64_pdf}" 
        },
        include_image_base64=True
        )
        return ocr_response

    def pdf2im(self, filepath:str):
        image_path:list[str] = []
        dir_name:str = os.path.dirname(filepath)
        with pymupdf.open(filepath) as doc:
            for idx in range(doc.page_count):
                pix = doc[idx].get_pixmap()
                temp_path = f"{filepath}_page_{idx}.png"
                pix.save(temp_path)
                image_path.append(temp_path)
        print("image_path:", image_path)
        return image_path[0]

    def bytes2bytes64(self, bytes):
        return base64.b64encode(bytes).decode('utf-8')

    def process_file(self, filepath:str):
        # convert the file to desired format
        image_path = self.pdf2im(filepath)
        return image_path

    def im2text(self, image):
        # # call the OCR
        ocr = PaddleOCR(
             use_doc_orientation_classify=False,
             use_doc_unwarping=False,
             use_textline_orientation=False,
         )

        paddle_result = ocr.predict(input=f"{image}")
        # post_process_paddle
        paddle_text = ["".join([text[0][0] for text in lin]) for lin in paddle_result]

        # tesseract
        #tesseract_result = pytesseract.image_to_data(
        #     Image.open(image), output_type="data.frame"
        #)
        # tesseract_text = tesseract_result["text"][
        #     (tesseract_result["text"].isna() == False)
        # ].to_list()
        # post process the results
        return paddle_text#, tesseract_text

    def doc2text(self, filepath:str, verbose:bool=1, result=[]):
        converter = DocumentConverter()
        doc = converter.convert(filepath).document
        markdown = doc.export_to_markdown()
        if verbose:
            md = Markdown(markdown)
            console.print(md)
        result.append(markdown)

    def agentic_parser(self, prompt:str):
        return

    def run_text_hrm(self, prompt):
        return

    def fastvlm_parser(self, base64_pdf):
        #TODO add the preprocessor for the pdf file to image converter
        import torch
        import sys
        sys.path.append("/Users/leonid/Desktop/HotCode/ml-fastvlm/")
        from llava.utils import disable_torch_init
        from llava.conversation import conv_templates
        from llava.model.builder import load_pretrained_model
        from llava.mm_utils import tokenizer_image_token, process_images, get_model_name_from_path
        from llava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN, DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN
        #tokenize the input prompts;
        model_path = "/Users/leonid/Desktop/HotCode/ml-fastvlm/checkpoints/llava-fastvithd_0.5b_stage3/"
        model_path = os.path.expanduser(model_path)
        
        model_base = None
        prompt = "Extract the text from given invoice"
        disable_torch_init()
        generation_config = None
        if os.path.exists(os.path.join(model_path, 'generation_config.json')):
            generation_config = os.path.join(model_path, '.generation_config.json')
            os.rename(os.path.join(model_path, 'generation_config.json'),
                    generation_config)
        model_name = get_model_name_from_path(model_path)
        tokenizer, model, image_processor, context_len = load_pretrained_model(model_path, 
                                                                               model_base, 
                                                                               model_name,
                                                                               device="mps")
        prompt = "Extract the text from given invoice"
        conv_mode = "qwen_2"
        qs = prompt
        if model.config.mm_use_im_start_end:
            qs = DEFAULT_IM_START_TOKEN + DEFAULT_IMAGE_TOKEN + DEFAULT_IM_END_TOKEN + '\n' + qs
        else:
            qs = DEFAULT_IMAGE_TOKEN + '\n' + qs
        conv = conv_templates[conv_mode].copy()
        conv.append_message(conv.roles[0], qs)
        conv.append_message(conv.roles[1], None)
        prompt = conv.get_prompt()

        # Set the pad token id for generation
        model.generation_config.pad_token_id = tokenizer.pad_token_id
        
        input_ids = tokenizer_image_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(0).to(torch.device("mps"))
        pdf_bytes = base64.b64decode(base64_pdf)
        print("Prompt:", prompt)
        image = Image.open(BytesIO(pdf_bytes))#.convert('RGB')
        image_tensor = process_images([image], image_processor, model.config)[0]
        temperature = 0.7
        top_p = 1
        num_beams = 1
        with torch.inference_mode():
            output_ids = model.generate(
                input_ids,
                images=image_tensor.unsqueeze(0).half(),
                image_sizes=[image.size],
                do_sample=True if temperature > 0 else False,
                temperature=temperature,
                top_p=top_p,
                num_beams=num_beams,
                max_new_tokens=256,
                use_cache=True)

            outputs = tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0].strip()
            print(outputs)
        #load the hugging face model -> 
        
        return outputs


