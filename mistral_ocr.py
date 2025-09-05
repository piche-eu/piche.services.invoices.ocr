import os
from mistralai import DocumentURLChunk
from mistralai import Mistral
import io

path = "/Users/leonid/Desktop/HotCode/Invoices/rēķini"

files = os.listdir(path)
api_key = "2ZdXjh2m4h37zfrvFUkhAFctFbxxM7py"
#api_key = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)


def encode_pdf(pdf_path):
    """Encode the pdf to base64."""
    try:
        with open(pdf_path, "rb") as pdf_file:
            return base64.b64encode(pdf_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {pdf_path} was not found.")
        return None
    except Exception as e:  # Added general exception handling
        print(f"Error: {e}")
        return None


def upload_file(file_path):
    uploaded_file = client.files.upload(
    file={
        "file_name": os.path.basename(file_path),
        "content":  open(file_path, "rb")
    },
    purpose="ocr",
    )
    signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)
    return signed_url

# Process a document via URL
def parse_ocr(base64_pdf):
    
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": f"data:application/pdf;base64,{base64_pdf}"
        },
        include_image_base64=True
    )

    return ocr_response

if __name__ == "__main__":
        #ocr_response = parse_ocr(file_path)
        # Upload the PDF file to Mistral's cloud storage
    pdf_path = "/Users/leonid/Desktop/HotCode/Invoices/rēķini/m_22.04-8.pdf" 

    signed_url = upload_file(pdf_path)
    #base64_pdf = encode_pdf(pdf_path)
    #ocr_response = parse_ocr(base64_pdf)
    # Process the uploaded document using the OCR model
    #print(ocr_response.markdown) 
    

    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document = DocumentURLChunk(document_url=signed_url.url),
        #document={
        #    "type": "document_url",
        #    "document_url": "https://arxiv.org/pdf/2201.04234"
        #},
        include_image_base64=True
    )

    print(ocr_response)# Access the extracted content in Markdown format
