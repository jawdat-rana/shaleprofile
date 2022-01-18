from fastapi import FastAPI
from routers import overview
from routers import eiaopendata
from fastapi.responses import HTMLResponse

app = FastAPI()
app.include_router(overview.router)
app.include_router(eiaopendata.router)


@app.get("/", response_class=HTMLResponse)
async def root():
    html = '''
        API Working - <a href="https://shale-gas-production.deta.dev/docs">Click Here</a> to check documentation
    '''
    return html
