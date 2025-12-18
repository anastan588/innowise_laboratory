from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from book_api import models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


@app.get("/healthcheck")
async def healthcheck() -> dict:
    return { "status": "ok"}

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    try:
        existing_book = (
            db.query(models.Book)
            .filter(models.Book.title == book.title, models.Book.author == book.author)
            .first()
        )
        if existing_book:
            raise HTTPException(
                status_code=400,
                detail="Book with this title and author already exists"
            )

        db_book = models.Book(title=book.title, author=book.author, year=book.year)
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Book with this title and author already exists"
        )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")



@app.get("/books/", response_model=list[schemas.Book])
def read_books(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1), db: Session = Depends(get_db)):
    try:
        offset = (page - 1) * page_size
        books = db.query(models.Book).offset(offset).limit(page_size).all()
        if not books:
            return []
        return books
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    try:
        book = db.query(models.Book).filter(models.Book.id == book_id).first()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        db.delete(book)
        db.commit()
        return book
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, updated_book: schemas.BookCreate, db: Session = Depends(get_db)):
    try:
        book = db.query(models.Book).filter(models.Book.id == book_id).first()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")

        book.title = updated_book.title
        book.author = updated_book.author
        book.year = updated_book.year

        db.commit()
        db.refresh(book)
        return book
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/books/search/", response_model=list[schemas.Book])
def search_books(
    title: str | None = None,
    author: str | None = None,
    year: int | None = None,
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(models.Book)

        if title:
            query = query.filter(models.Book.title.ilike(f"%{title}%"))
        if author:
            query = query.filter(models.Book.author.ilike(f"%{author}%"))
        if year:
            query = query.filter(models.Book.year == year)

        offset = (page - 1) * page_size
        results = query.offset(offset).limit(page_size).all()

        if not results:
            return []
        return results
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

