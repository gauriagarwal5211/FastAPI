from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from .database import create_db_and_tables, get_session
from .models import Item, ItemCreate, ItemUpdate, StatusEnum


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Campus Lost & Found API",
    description="REST API for managing lost and found items on campus.",
    version="1.0.0",
    lifespan=lifespan,
)


# 1. CREATE ITEM
@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(
    item_data: ItemCreate,
    session: Session = Depends(get_session),
):
    item = Item.model_validate(item_data)

    session.add(item)
    session.commit()
    session.refresh(item)

    return item

# 2. GET ALL ITEMS
@app.get("/items", response_model=list[Item])
def get_items(
    session: Session = Depends(get_session),
):
    statement = select(Item)
    items = session.exec(statement).all()

    return items


# 3. GET ITEM BY ID
@app.get("/items/{item_id}", response_model=Item)
def get_item(
    item_id: int,
    session: Session = Depends(get_session),
):
    item = session.get(Item, item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    return item


# 4. UPDATE ITEM
@app.put("/items/{item_id}", response_model=Item)
def update_item(
    item_id: int,
    item_data: ItemUpdate,
    session: Session = Depends(get_session),
):
    item = session.get(Item, item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    item.title = item_data.title
    item.description = item_data.description
    item.category = item_data.category
    item.location = item_data.location
    item.reported_by = item_data.reported_by
    item.status = item_data.status

    session.add(item)
    session.commit()
    session.refresh(item)

    return item


# 5. DELETE ITEM
@app.delete("/items/{item_id}")
def delete_item(
    item_id: int,
    session: Session = Depends(get_session),
):
    item = session.get(Item, item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    session.delete(item)
    session.commit()

    return {
        "message": "Item deleted successfully",
    }


# 6. FILTER BY STATUS
@app.get("/items/status/{status}", response_model=list[Item])
def get_items_by_status(
    status: StatusEnum,
    session: Session = Depends(get_session),
):
    statement = select(Item).where(Item.status == status)
    items = session.exec(statement).all()

    return items


# 7. FILTER BY CATEGORY
@app.get("/items/category/{category}", response_model=list[Item])
def get_items_by_category(
    category: str,
    session: Session = Depends(get_session),
):
    statement = select(Item).where(Item.category == category)
    items = session.exec(statement).all()

    return items