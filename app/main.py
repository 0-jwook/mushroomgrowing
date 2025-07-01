from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .crud import *

app = FastAPI()

# Pydantic 모델 정의
class MushroomCreate(BaseModel):
    name: str

templates = Jinja2Templates(directory="app/templates")  # 템플릿 폴더 위치에 맞게 수정
app.mount("/static", StaticFiles(directory="app/templates/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    mushrooms = get_all_mushrooms()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "mushrooms": mushrooms
    })

@app.get("/mushroom/{m_id}", response_class=HTMLResponse)
def mushroom_detail(request: Request, m_id: int):
    mushroom = get_mushroom_by_id(m_id)
    if not mushroom:
        return RedirectResponse("/", status_code=302)
    return templates.TemplateResponse("mushroom.html", {"request": request, "mushroom": mushroom})

@app.post("/mushroom/{m_id}/upgrade")
def upgrade_mushroom_view(request: Request, m_id: int):
    result = upgrade_mushroom(m_id)
    if result["broken"]:
        return templates.TemplateResponse("fail.html", {
            "request": request
        })
    else:
        mushroom = get_mushroom_by_id(m_id)
        return RedirectResponse(f"/mushroom/{mushroom.id}", status_code=303)

@app.post("/mushroom/{m_id}/delete")
def delete_mushroom_view(m_id: int):
    delete_mushroom(m_id)
    return RedirectResponse("/", status_code=303)


@app.delete("/delete/{m_id}")
def delete(m_id: int):
    success = delete_mushroom(m_id)
    if not success:
        raise HTTPException(status_code=404, detail="Mushroom not found")
        return {"message": f"Mushroom {m_id} deleted successfully"}

@app.get("/create", response_class=HTMLResponse)
def show_create_page(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@app.post("/create")
def create_mushroom_view(name: str = Form(...)):
    create_mushroom(name)
    return RedirectResponse("/", status_code=303)

# @app.post("/create")
# def create(mushroom: MushroomCreate):
#     print("debug")
#     create_mushroom(mushroom.name)
#     return RedirectResponse("/", status_code=303)