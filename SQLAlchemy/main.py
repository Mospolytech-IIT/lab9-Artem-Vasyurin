from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User, Post
from pydantic import BaseModel
from fastapi import Request
from fastapi.responses import RedirectResponse

app = FastAPI()

# Подключаем Jinja2 для работы с шаблонами
templates = Jinja2Templates(directory="templates")

# Создание таблиц в базе данных (если они еще не созданы)
Base.metadata.create_all(bind=engine)

# Сессия для работы с базой данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Страница для отображения списка пользователей
@app.get("/users/", response_class=HTMLResponse)
async def users_list(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("users_list.html", {"request": request, "users": users})

# Страница для создания нового пользователя
@app.get("/users/create", response_class=HTMLResponse)
async def create_user_form(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})

@app.post("/users/", response_class=HTMLResponse)
async def create_user(username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = User(username=username, email=email, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return HTMLResponse(content=f"User {username} created successfully! <a href='/users/'>Back to Users List</a>")

# Страница для редактирования пользователя
@app.get("/users/{user_id}/edit", response_class=HTMLResponse)
async def edit_user_form(user_id: int, request: Request, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("edit_user.html", {"request": request, "user": db_user})

@app.post("/users/{user_id}/edit", response_class=HTMLResponse)
async def update_user(user_id: int, username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = username
    db_user.email = email
    db_user.password = password
    db.commit()
    db.refresh(db_user)
    return HTMLResponse(content=f"User {username} updated successfully! <a href='/users/'>Back to Users List</a>")

# Страница для удаления пользователя
@app.get("/users/{user_id}/delete", response_class=HTMLResponse)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return HTMLResponse(content=f"User {db_user.username} deleted successfully! <a href='/users/'>Back to Users List</a>")

# Страница для отображения списка постов
@app.get("/posts/", response_class=HTMLResponse)
async def posts_list(request: Request, db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return templates.TemplateResponse("posts_list.html", {"request": request, "posts": posts})

# Страница для создания нового поста
@app.get("/posts/create", response_class=HTMLResponse)
async def create_post_form(request: Request):
    return templates.TemplateResponse("create_post.html", {"request": request})

@app.post("/posts/", response_class=HTMLResponse)
async def create_post(title: str = Form(...), content: str = Form(...), db: Session = Depends(get_db)):
    db_post = Post(title=title, content=content, user_id=1)  # Пример для пользователя с id = 1
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return HTMLResponse(content=f"Post '{title}' created successfully! <a href='/posts/'>Back to Posts List</a>")

# Страница для редактирования поста
@app.get("/posts/{post_id}/edit", response_class=HTMLResponse)
async def edit_post_form(post_id: int, request: Request, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return templates.TemplateResponse("edit_post.html", {"request": request, "post": db_post})


@app.post("/posts/{post_id}/update", response_class=HTMLResponse)
async def update_post(post_id: int, title: str = Form(...), content: str = Form(...), db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    db_post.title = title
    db_post.content = content
    db.commit()
    db.refresh(db_post)
    return RedirectResponse(url="/posts/", status_code=303)

# Страница для удаления поста
@app.get("/posts/{post_id}/delete", response_class=HTMLResponse)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return HTMLResponse(content=f"Post '{db_post.title}' deleted successfully! <a href='/posts/'>Back to Posts List</a>")
