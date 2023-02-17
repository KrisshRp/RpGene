import uvicorn, os, app
from Lib import loadenv

loadenv()
if __name__ == "__main__":
    print(os.getenv('APP_PORT'))
    uvicorn.run("app:app", port=int(os.getenv('APP_PORT')))