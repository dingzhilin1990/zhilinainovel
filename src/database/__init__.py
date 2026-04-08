"""
Database module for zhilinainovel
基因库和素材库管理
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./zhilinainovel.db")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ============ Database Models ============

class NovelOutline(Base):
    """小说大纲"""
    __tablename__ = "novel_outlines"

    id = Column(Integer, primary_key=True, autoincrement=True)
    genre = Column(String(50))          # 题材
    theme = Column(String(200))         # 主题
    main_char = Column(String(100))    # 主角
    length = Column(String(20))        # 篇幅
    outline = Column(Text)              # 大纲内容
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "genre": self.genre,
            "theme": self.theme,
            "main_char": self.main_char,
            "length": self.length,
            "outline": self.outline,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Chapter(Base):
    """章节"""
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    outline_id = Column(Integer)        # 关联大纲
    chapter_num = Column(Integer)       # 章节号
    content = Column(Text)              # 章节内容
    word_count = Column(Integer)       # 字数
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "outline_id": self.outline_id,
            "chapter_num": self.chapter_num,
            "content": self.content,
            "word_count": self.word_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class GeneTemplate(Base):
    """基因模板"""
    __tablename__ = "gene_templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    genre = Column(String(50))          # 题材
    name = Column(String(200))          # 基因名称
    elements = Column(JSON)             # 核心要素列表
    excitement = Column(JSON)           # 爽点列表
    structure = Column(String(50))     # 结构模式
    keywords = Column(JSON)            # 关键词
    style_notes = Column(Text)          # 风格备注
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "genre": self.genre,
            "name": self.name,
            "elements": self.elements,
            "excitement": self.excitement,
            "structure": self.structure,
            "keywords": self.keywords,
            "style_notes": self.style_notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class GoldenSentence(Base):
    """金句库"""
    __tablename__ = "golden_sentences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    genre = Column(String(50))          # 题材
    sentence = Column(Text)            # 金句内容
    source = Column(String(200))       # 来源
    tags = Column(JSON)                # 标签
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "genre": self.genre,
            "sentence": self.sentence,
            "source": self.source,
            "tags": self.tags,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# ============ Database Operations ============

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session (dependency injection style)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============ CRUD Operations ============

def save_outline(genre: str, theme: str, main_char: str, length: str, outline: str):
    """保存大纲"""
    init_db()
    db = SessionLocal()
    try:
        obj = NovelOutline(genre=genre, theme=theme, main_char=main_char, length=length, outline=outline)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj.to_dict()
    finally:
        db.close()


def save_chapter(outline_id: int, chapter_num: int, content: str, word_count: int):
    """保存章节"""
    init_db()
    db = SessionLocal()
    try:
        obj = Chapter(outline_id=outline_id, chapter_num=chapter_num, content=content, word_count=word_count)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj.to_dict()
    finally:
        db.close()


def list_outlines(limit: int = 20):
    """列出最近的大纲"""
    init_db()
    db = SessionLocal()
    try:
        results = db.query(NovelOutline).order_by(NovelOutline.created_at.desc()).limit(limit).all()
        return [r.to_dict() for r in results]
    finally:
        db.close()


def search_genes(genre: str = None, keyword: str = None):
    """搜索基因模板"""
    init_db()
    db = SessionLocal()
    try:
        query = db.query(GeneTemplate)
        if genre:
            query = query.filter(GeneTemplate.genre == genre)
        if keyword:
            query = query.filter(GeneTemplate.name.contains(keyword))
        results = query.all()
        return [r.to_dict() for r in results]
    finally:
        db.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized: zhilinainovel.db")
    print("Tables: novel_outlines, chapters, gene_templates, golden_sentences")
