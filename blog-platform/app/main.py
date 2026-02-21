from pathlib import Path
from datetime import datetime, timezone
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db, create_tables, Base, engine, SessionLocal

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey


class PostModel(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class CommentModel(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    author = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class PostCreate(BaseModel):
    title: str
    content: str
    author: str


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    author: str | None = None


class CommentCreate(BaseModel):
    author: str
    content: str


class CommentUpdate(BaseModel):
    author: str | None = None
    content: str | None = None


create_tables()

app = FastAPI(title="Blog API")

static_dir = Path(__file__).resolve().parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/")
def index():
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "Blog API. Open /static/index.html or mount static folder."}


@app.get("/api/posts")
def list_posts(db: Session = Depends(get_db)):
    posts = db.query(PostModel).order_by(PostModel.created_at.desc()).all()
    return [
        {
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "author": p.author,
            "created_at": p.created_at.isoformat() if p.created_at else None,
        }
        for p in posts
    ]


@app.get("/api/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author": post.author,
        "created_at": post.created_at.isoformat() if post.created_at else None,
    }


@app.post("/api/posts", status_code=201)
def create_post(data: PostCreate, db: Session = Depends(get_db)):
    post = PostModel(title=data.title, content=data.content, author=data.author)
    db.add(post)
    db.commit()
    db.refresh(post)
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author": post.author,
        "created_at": post.created_at.isoformat() if post.created_at else None,
    }


@app.put("/api/posts/{post_id}")
def update_post(post_id: int, data: PostUpdate, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if data.title is not None:
        post.title = data.title
    if data.content is not None:
        post.content = data.content
    if data.author is not None:
        post.author = data.author
    db.commit()
    db.refresh(post)
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author": post.author,
        "created_at": post.created_at.isoformat() if post.created_at else None,
    }


@app.delete("/api/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return Response(status_code=204)


@app.get("/api/posts/{post_id}/comments")
def list_comments(post_id: int, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comments = db.query(CommentModel).filter(CommentModel.post_id == post_id).order_by(CommentModel.created_at).all()
    return [
        {
            "id": c.id,
            "post_id": c.post_id,
            "author": c.author,
            "content": c.content,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        }
        for c in comments
    ]


@app.post("/api/posts/{post_id}/comments", status_code=201)
def create_comment(post_id: int, data: CommentCreate, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comment = CommentModel(post_id=post_id, author=data.author, content=data.content)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return {
        "id": comment.id,
        "post_id": comment.post_id,
        "author": comment.author,
        "content": comment.content,
        "created_at": comment.created_at.isoformat() if comment.created_at else None,
    }


@app.put("/api/posts/{post_id}/comments/{comment_id}")
def update_comment(
    post_id: int, comment_id: int, data: CommentUpdate, db: Session = Depends(get_db)
):
    comment = (
        db.query(CommentModel)
        .filter(CommentModel.id == comment_id, CommentModel.post_id == post_id)
        .first()
    )
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if data.author is not None:
        comment.author = data.author
    if data.content is not None:
        comment.content = data.content
    db.commit()
    db.refresh(comment)
    return {
        "id": comment.id,
        "post_id": comment.post_id,
        "author": comment.author,
        "content": comment.content,
        "created_at": comment.created_at.isoformat() if comment.created_at else None,
    }


@app.delete("/api/posts/{post_id}/comments/{comment_id}")
def delete_comment(post_id: int, comment_id: int, db: Session = Depends(get_db)):
    comment = (
        db.query(CommentModel)
        .filter(CommentModel.id == comment_id, CommentModel.post_id == post_id)
        .first()
    )
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(comment)
    db.commit()
    return Response(status_code=204)
