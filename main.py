from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests, zipfile, io, xml.etree.ElementTree as ET

app = FastAPI()

LOGIN = "09229746000146"
SENHA = "684341"
URL = "https://webservice.newrastreamentoonline.com.br"

@app.get("/telemetria")
def get_telemetria():
    xml_request = f"<RequestTelemetria><login>{LOGIN}</login><senha>{SENHA}</senha></RequestTelemetria>"
    headers = {"Content-Type": "application/xml"}
    response = requests.post(URL, data=xml_request.encode("utf-8"), headers=headers)

    if response.status_code != 200:
        return JSONResponse(content={"erro": f"Erro HTTP: {response.status_code}"}, status_code=500)

    try:
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
        xml_content = zip_file.read(zip_file.namelist()[0])
        root = ET.fromstring(xml_content)
        dados = [{el.tag: el.text for el in registro} for registro in root]
        return dados

    except Exception as e:
        return JSONResponse(content={
            "erro": "A resposta da API não é um arquivo ZIP ou XML válido.",
            "detalhe": str(e)
        }, status_code=500)
