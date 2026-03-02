from fastapi import FastAPI,Request,Form,HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

v_username = "admin"
v_password = "Admin@123"

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def login_form(req: Request):
    return templates.TemplateResponse("login.html", {"request": req})

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    if username == v_username and password == v_password:
        return {"message":"Login Successful!!!"}
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password")