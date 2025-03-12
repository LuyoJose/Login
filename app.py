from fastapi import FastAPI, HTTPException, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret_key")

users = {}  # Almacenamiento en memoria

# Configurar templates y archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user = request.session.get("user")
    if user:
        return templates.TemplateResponse(request, "home.html", {"username": user})
    return templates.TemplateResponse(request, "login.html")

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username in users and users[username] == password:
        request.session["user"] = username
        return RedirectResponse(url="/", status_code=303)  # Asegurar la redirección
    raise HTTPException(status_code=400, detail="Credenciales incorrectas")

@app.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse(request, "register.html")

@app.post("/register")
async def register(username: str = Form(...), password: str = Form(...)):
    if username in users:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    users[username] = password
    return RedirectResponse(url="/", status_code=303)  # Asegurar la redirección


@app.get("/logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/", status_code=303)  # Asegurar la redirección

