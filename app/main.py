from fastapi import FastAPI, Request, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from .database import init_db, get_db

app = FastAPI(title="🗄️ خزانتي الرقمية", version="1.0.0")

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Initialize database on startup
@app.on_event("startup")
def startup():
    init_db()

# ==================== HOME ====================
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, lang: str = "ar"):
    conn = get_db()
    articles = conn.execute("SELECT * FROM articles ORDER BY created_at DESC LIMIT 10").fetchall()
    notes = conn.execute("SELECT * FROM notes ORDER BY pinned DESC, created_at DESC LIMIT 5").fetchall()
    categories = conn.execute("SELECT DISTINCT category FROM articles").fetchall()
    conn.close()
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "articles": articles,
        "notes": notes,
        "categories": categories,
        "lang": lang
    })

# ==================== ARTICLES ====================
@app.get("/articles", response_class=HTMLResponse)
async def list_articles(request: Request, category: str = "", search: str = "", lang: str = "ar"):
    conn = get_db()
    
    if search:
        articles = conn.execute(
            "SELECT * FROM articles WHERE title LIKE ? OR content LIKE ? OR tags LIKE ? ORDER BY created_at DESC",
            (f"%{search}%", f"%{search}%", f"%{search}%")
        ).fetchall()
    elif category:
        articles = conn.execute(
            "SELECT * FROM articles WHERE category = ? ORDER BY created_at DESC",
            (category,)
        ).fetchall()
    else:
        articles = conn.execute("SELECT * FROM articles ORDER BY created_at DESC").fetchall()
    
    categories = conn.execute("SELECT DISTINCT category FROM articles").fetchall()
    conn.close()
    
    return templates.TemplateResponse("articles.html", {
        "request": request,
        "articles": articles,
        "categories": categories,
        "current_category": category,
        "search_query": search,
        "lang": lang
    })

@app.get("/articles/new", response_class=HTMLResponse)
async def new_article_form(request: Request, lang: str = "ar"):
    return templates.TemplateResponse("article_form.html", {
        "request": request,
        "article": None,
        "lang": lang
    })

@app.get("/articles/{article_id}", response_class=HTMLResponse)
async def view_article(request: Request, article_id: int, lang: str = "ar"):
    conn = get_db()
    article = conn.execute("SELECT * FROM articles WHERE id = ?", (article_id,)).fetchone()
    conn.close()
    
    if not article:
        return RedirectResponse("/articles")
    
    return templates.TemplateResponse("article_view.html", {
        "request": request,
        "article": article,
        "lang": lang
    })

@app.post("/articles/create")
async def create_article(
    title: str = Form(...),
    content: str = Form(...),
    category: str = Form("عام"),
    tags: str = Form(""),
    language: str = Form("ar")
):
    conn = get_db()
    conn.execute(
        "INSERT INTO articles (title, content, category, tags, language) VALUES (?, ?, ?, ?, ?)",
        (title, content, category, tags, language)
    )
    conn.commit()
    conn.close()
    return RedirectResponse("/articles", status_code=303)

@app.get("/articles/{article_id}/edit", response_class=HTMLResponse)
async def edit_article_form(request: Request, article_id: int, lang: str = "ar"):
    conn = get_db()
    article = conn.execute("SELECT * FROM articles WHERE id = ?", (article_id,)).fetchone()
    conn.close()
    
    return templates.TemplateResponse("article_form.html", {
        "request": request,
        "article": article,
        "lang": lang
    })

@app.post("/articles/{article_id}/update")
async def update_article(
    article_id: int,
    title: str = Form(...),
    content: str = Form(...),
    category: str = Form("عام"),
    tags: str = Form(""),
    language: str = Form("ar")
):
    conn = get_db()
    conn.execute(
        "UPDATE articles SET title=?, content=?, category=?, tags=?, language=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
        (title, content, category, tags, language, article_id)
    )
    conn.commit()
    conn.close()
    return RedirectResponse(f"/articles/{article_id}", status_code=303)

@app.post("/articles/{article_id}/delete")
async def delete_article(article_id: int):
    conn = get_db()
    conn.execute("DELETE FROM articles WHERE id = ?", (article_id,))
    conn.commit()
    conn.close()
    return RedirectResponse("/articles", status_code=303)

# ==================== NOTES ====================
@app.get("/notes", response_class=HTMLResponse)
async def list_notes(request: Request, lang: str = "ar"):
    conn = get_db()
    notes = conn.execute("SELECT * FROM notes ORDER BY pinned DESC, created_at DESC").fetchall()
    conn.close()
    
    return templates.TemplateResponse("notes.html", {
        "request": request,
        "notes": notes,
        "lang": lang
    })

@app.get("/notes/new", response_class=HTMLResponse)
async def new_note_form(request: Request, lang: str = "ar"):
    return templates.TemplateResponse("note_form.html", {
        "request": request,
        "note": None,
        "lang": lang
    })

@app.post("/notes/create")
async def create_note(
    title: str = Form(...),
    content: str = Form(...),
    pinned: int = Form(0)
):
    conn = get_db()
    conn.execute(
        "INSERT INTO notes (title, content, pinned) VALUES (?, ?, ?)",
        (title, content, pinned)
    )
    conn.commit()
    conn.close()
    return RedirectResponse("/notes", status_code=303)

@app.post("/notes/{note_id}/delete")
async def delete_note(note_id: int):
    conn = get_db()
    conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
    return RedirectResponse("/notes", status_code=303)

# ==================== SEARCH ====================
@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str = "", lang: str = "ar"):
    conn = get_db()
    articles = []
    notes = []
    
    if q:
        articles = conn.execute(
            "SELECT * FROM articles WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?",
            (f"%{q}%", f"%{q}%", f"%{q}%")
        ).fetchall()
        notes = conn.execute(
            "SELECT * FROM notes WHERE title LIKE ? OR content LIKE ?",
            (f"%{q}%", f"%{q}%")
        ).fetchall()
    
    conn.close()
    
    return templates.TemplateResponse("search.html", {
        "request": request,
        "query": q,
        "articles": articles,
        "notes": notes,
        "lang": lang
    })

# ==================== API for adding articles ====================
@app.post("/api/articles")
async def api_create_article(
    title: str = Form(...),
    content: str = Form(...),
    category: str = Form("عام"),
    tags: str = Form(""),
    language: str = Form("ar")
):
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO articles (title, content, category, tags, language) VALUES (?, ?, ?, ?, ?)",
        (title, content, category, tags, language)
    )
    article_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {"ok": True, "id": article_id, "message": "Article created"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
