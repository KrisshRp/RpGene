import json, sys, uvicorn, os
from Lib import NCBIscraper, createZip
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, WebSocket

app = FastAPI()
app.mount("/Bin/Assets/", StaticFiles(directory="./Bin/Assets"), name="static")
templates = Jinja2Templates(directory="./Bin/Templates")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    a = await websocket.accept()
    d = await websocket.receive()
    species = json.loads(d["text"])
    species["locustags"] = [i for i in species["locustags"].replace('"',"").replace("\n"," ").replace(" ",",").split(",") if i != ""]
    print(species)
    obj = NCBIscraper(species['organismname'], species['accessionnum'], species["locustags"], log=False, headless=True)
    for responce in obj.run():
        await websocket.send_json(responce)
        sys.stdout.write("\r"+ f"{responce}")
        sys.stdout.flush()

@app.get("/download/{Accession}")
def main(Accession=""):
    foldername = f"./Temp/scrapdata/{Accession}"
    fileName = f"{Accession}"
    downloadpath = createZip(folderpath=foldername, fileName=fileName)
    return FileResponse(path=downloadpath, filename=f"{fileName}.zip", media_type='zip')
