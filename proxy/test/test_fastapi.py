import base64
import requests
import argparse
parser = argparse.ArgumentParser(
                    prog='Test Invoice Parsig',
                    epilog='Text at the bottom of help')

filepath = parser.add_argument('filename')
args = parser.parse_args()
filepath = args.filename

# Example: Encoding a file
with open(filepath, "rb") as image_file:
    encoded_string = image_file.read()
    encoded_string = base64.b64encode(encoded_string).decode("utf-8")

url = "http://127.0.0.1:8000/upload-base64-file/"  # Replace with your FastAPI server address
payload = {"data": encoded_string, "filename": "test.pdf"}
headers = {"Content-Type": "application/json"}
response = requests.post(url, json=payload, headers=headers)
print(response.json())
