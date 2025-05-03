from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional, List, Literal
from src.schemas.subjects import SubjectMeta, SubjectStatModel, PyObjectId, SubjectBulkCreateResponse
from src.db import db
from bson import ObjectId
from pydantic import TypeAdapter

router = APIRouter()


@router.get("/", response_model=List[SubjectMeta])
async def get_all_subjects(
        subject_name: Optional[str] = Query(None),
        limit: Optional[int] = Query(10, gt=0),
        offset: Optional[int] = Query(0, ge=0),
        sort_by: Optional[str] = Query("name"),
        order: Optional[Literal["asc", "desc"]] = Query("asc")
):
    query = {}
    if subject_name:
        query["name"] = {"$regex": subject_name, "$options": "i"}

    sort_order = 1 if order == "asc" else -1
    sort_field = sort_by if sort_by in ["name", "description"] else "name"
    subjects_cursor = db.subjects.find(query).sort(sort_field, sort_order).skip(offset).limit(limit)
    subjects = await subjects_cursor.to_list(length=None)
    for subject in subjects:
        subject["_id"] = str(subject["_id"])

    adapter = TypeAdapter(List[SubjectMeta])
    return adapter.validate_python(subjects)


@router.post("/", response_model=SubjectMeta, status_code=status.HTTP_201_CREATED)
async def create_subject(subject: SubjectMeta):
    try:
        subject_dict = subject.model_dump(by_alias=True, exclude={"id"})
        result = await db.subjects.insert_one(subject_dict)
        created_subject = await db.subjects.find_one({"_id": result.inserted_id})

        if created_subject and "_id" in created_subject:
            created_subject["_id"] = str(created_subject["_id"])

        return created_subject
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database operation failed: {str(e)}"
        )


@router.get("/{subject_id}", response_model=SubjectMeta)
async def get_subject(subject_id: str):
    if not ObjectId.is_valid(subject_id):
        raise HTTPException(status_code=400, detail="Invalid subject ID")

    subject = await db.subjects.find_one({"_id": ObjectId(subject_id)})
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    subject["_id"] = str(subject["_id"])
    return TypeAdapter(SubjectMeta).validate_python(subject)


@router.patch("/{subject_id}", response_model=SubjectMeta)
async def update_subject(subject_id: str, subject: SubjectMeta):
    if not ObjectId.is_valid(subject_id):
        raise HTTPException(status_code=400, detail="Invalid subject ID")

    existing = await db.subjects.find_one({"_id": ObjectId(subject_id)})
    if not existing:
        raise HTTPException(status_code=404, detail="Subject not found")

    update_data = subject.model_dump(by_alias=True, exclude_unset=True)
    await db.subjects.update_one({"_id": ObjectId(subject_id)}, {"$set": update_data})

    updated = await db.subjects.find_one({"_id": ObjectId(subject_id)})
    updated["_id"] = str(updated["_id"])

    return TypeAdapter(SubjectMeta).validate_python(updated)


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subject(subject_id: str):
    if not ObjectId.is_valid(subject_id):
        raise HTTPException(status_code=400, detail="Invalid subject ID")

    result = await db.subjects.delete_one({"_id": ObjectId(subject_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Subject not found")


@router.post(
    "/bulk/",
    response_model=SubjectBulkCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Bulk create subjects",
    tags=["subjects", "bulk"]
)
async def bulk_create_subjects(subjects: list[SubjectMeta]):
    try:
        subjects_dicts = [subject.model_dump(by_alias=True, exclude_none=True, exclude={"id"})
                          for subject in subjects]
        result = await db.subjects.insert_many(subjects_dicts)
        return SubjectBulkCreateResponse(inserted_ids=[str(id) for id in result.inserted_ids])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Bulk create operation failed: {str(e)}"
        )
