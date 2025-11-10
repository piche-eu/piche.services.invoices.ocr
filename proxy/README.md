#### Piche Invoice OCR Proxy Server

### Prepare the env variables
```
cd ./proxy/ocr 
In the .env file add line:
export MISTRAL_API = <API KEY>
```


### Run using Docker:
```
docker compose up
docker run -it ollama ollama pull deepseek-r1:1.5b
```


### Local test:
```
cd ./proxy/test
python3 test_fastapi.py <filename.pdf>
```
