from sqlalchemy import Column, Integer, String, UniqueConstraint
from .database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True) 
    title = Column(String, nullable=False, default="Untitled")
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=True)
    
    __table_args__ = (
        UniqueConstraint("title", "author", name="uq_book_title_author"),
    )

