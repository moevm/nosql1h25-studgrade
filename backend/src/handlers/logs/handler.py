from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional, Literal
from src.schemas.logs import LogModel, LogCreate, LogUpdate, LogBulkCreateResponse
from src.db import db
from bson import ObjectId
from pydantic import TypeAdapter
from datetime import date

router = APIRouter()


@router.get("/", response_model=list[LogModel])
async def get_all_logs(
        limit: Optional[int] = Query(10, gt=0),
        offset: Optional[int] = Query(0, ge=0),
        sort_by: Optional[str] = Query("action_date"),
        order: Optional[Literal["asc", "desc"]] = Query("desc"),
        action_type: Optional[str] = Query(None),
        affected_entity: Optional[str] = Query(None),
        start_date: Optional[date] = Query(None),
        end_date: Optional[date] = Query(None)
):
    query = {}

    if action_type:
        query["action_type"] = {"$regex": action_type, "$options": "i"}
    if affected_entity:
        query["affected_entity"] = {"$regex": affected_entity, "$options": "i"}
    if start_date and end_date:
        query["action_date"] = {"$gte": start_date, "$lte": end_date}
    elif start_date:
        query["action_date"] = {"$gte": start_date}
    elif end_date:
        query["action_date"] = {"$lte": end_date}

    sort_order = 1 if order == "asc" else -1
    sort_field = sort_by if sort_by in ["action_date", "action_type", "affected_entity"] else "action_date"

    logs_cursor = db.logs.find(query).sort(sort_field, sort_order).skip(offset).limit(limit)
    logs = await logs_cursor.to_list(length=None)

    for log in logs:
        log["_id"] = str(log["_id"])

    adapter = TypeAdapter(list[LogModel])
    return adapter.validate_python(logs)


@router.post("/", response_model=LogModel, status_code=status.HTTP_201_CREATED)
async def create_log(log: LogCreate):
    try:
        log_dict = log.model_dump(by_alias=True, exclude={"id"})

        if 'action_date' in log_dict and isinstance(log_dict['action_date'], date):
            from datetime import datetime
            log_dict['action_date'] = datetime.combine(log_dict['action_date'], datetime.min.time())

        result = await db.logs.insert_one(log_dict)
        created_log = await db.logs.find_one({"_id": result.inserted_id})

        if created_log:
            created_log["_id"] = str(created_log["_id"])
            if 'action_date' in created_log:
                created_log['action_date'] = created_log['action_date'].date()

        return created_log
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database operation failed: {str(e)}"
        )


@router.get("/{log_id}", response_model=LogModel)
async def get_log(log_id: str):
    if not ObjectId.is_valid(log_id):
        raise HTTPException(status_code=400, detail="Invalid log ID")

    log = await db.logs.find_one({"_id": ObjectId(log_id)})
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")

    log["_id"] = str(log["_id"])
    return TypeAdapter(LogModel).validate_python(log)


@router.patch("/{log_id}", response_model=LogModel)
async def update_log(log_id: str, log: LogUpdate):
    if not ObjectId.is_valid(log_id):
        raise HTTPException(status_code=400, detail="Invalid log ID")

    existing = await db.logs.find_one({"_id": ObjectId(log_id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Log not found")

    update_data = log.model_dump(by_alias=True, exclude_unset=True)
    await db.logs.update_one({"_id": ObjectId(log_id)}, {"$set": update_data})

    updated = await db.logs.find_one({"_id": ObjectId(log_id)})
    updated["_id"] = str(updated["_id"])

    return TypeAdapter(LogModel).validate_python(updated)


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_log(log_id: str):
    if not ObjectId.is_valid(log_id):
        raise HTTPException(status_code=400, detail="Invalid log ID")

    result = await db.logs.delete_one({"_id": ObjectId(log_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Log not found")


@router.post(
    "/bulk/",
    response_model=LogBulkCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Bulk create logs",
    tags=["logs", "bulk"]
)
async def bulk_create_logs(logs: list[LogCreate]):
    try:
        logs_dicts = []
        for log in logs:
            log_dict = log.model_dump(by_alias=True, exclude_none=True)
            if isinstance(log_dict.get("action_date"), date):
                log_dict["action_date"] = log_dict["action_date"].isoformat()
            logs_dicts.append(log_dict)

        result = await db.logs.insert_many(logs_dicts)
        return LogBulkCreateResponse(inserted_ids=[str(id) for id in result.inserted_ids])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Bulk create operation failed: {str(e)}"
        )