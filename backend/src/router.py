from http.client import InvalidURL
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException
from .database import AsyncDep, get_database
from .models import Item, ItemUpdate
from .schemas import ItemResponse, ItemsResponse
from motor.core import AgnosticDatabase

router = APIRouter()


@router.post("/items/", response_model=ItemResponse)
async def create_item(item: Item, db: AsyncDep):
    item_dict = item.model_dump()
    result = await db["items"].insert_one(item_dict)
    created_item = await db["items"].find_one({"_id": result.inserted_id})
    return ItemResponse(**created_item, id=str(created_item["_id"]))


@router.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: str, db: AsyncDep):
    try:
        obj_id = ObjectId(item_id)
    except InvalidURL:
        raise HTTPException(status_code=404, detail="Invalid item ID")

    item = await db["items"].find_one({"_id": obj_id})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return ItemResponse(**item, id=str(item["_id"]))


@router.get("/items/", response_model=ItemsResponse)
async def read_items(db: AsyncDep):
    items = await db["items"].find().to_list(length=None)
    return ItemsResponse(
        items=[ItemResponse(**item, id=str(item["_id"])) for item in items]
    )


@router.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: str, updated_item: ItemUpdate, db: AsyncDep):
    try:
        obj_id = ObjectId(item_id)
    except InvalidId:
        raise HTTPException(status_code=404, detail="Invalid item ID")

    # Формируем запрос на обновление только тех полей, которые указаны
    update_data = updated_item.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")

    # Выполняем обновление
    result = await db["items"].update_one({"_id": obj_id}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Item not found or no changes made")

    # Получаем обновленный элемент
    updated = await db["items"].find_one({"_id": obj_id})
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found after update")

    return ItemResponse(**updated, id=str(updated["_id"]))


@router.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: str, db: AsyncDep):
    try:
        obj_id = ObjectId(item_id)
    except InvalidId:
        raise HTTPException(status_code=404, detail="Invalid item ID")

    deleted = await db["items"].delete_one({"_id": obj_id})
    if deleted.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
