from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from pydantic import ValidationError

from src.db.dependencies import get_teachers_collection, get_users_collection
from src.exceptions import UserAlreadyExistsError, UserNotFoundError
from src.schemas.teachers import (

    TeacherWithUserResponseSchema,
    TeacherCreateSchema,
    TeacherUpdateSchema
)

from src.models.TeacherModel import TeacherModel
from src.repositories import teacher_repository
from src.query_params import get_pagination_params, PaginationParams
from src.query_params.teacher_params import (
    TeacherFilterParams,
    TeacherSortParams,
    get_teacher_sort_params,
    get_teacher_filter_params
)

router = APIRouter()



@router.get("/", response_model=list[TeacherWithUserResponseSchema])
async def list_teachers_endpoint(
    teacher_filters: TeacherFilterParams = Depends(get_teacher_filter_params),  # type: ignore
    pagination: PaginationParams = Depends(get_pagination_params),
    sort: TeacherSortParams = Depends(get_teacher_sort_params),
    teachers_collection=Depends(get_teachers_collection),
):
    teacher_models = await teacher_repository.get_list_teachers(
        teacher_filters, sort, pagination, teachers_collection
    )
    try:
        return [teacher.to_response_schema() for teacher in teacher_models]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal error while serializing teachers: " + str(e),
        )


@router.post(
    "/",
    response_model=TeacherWithUserResponseSchema,
    status_code=status.HTTP_201_CREATED,
    tags=["teachers"],
)
async def create_teacher(
    teacher: TeacherCreateSchema,
    teachers_collection=Depends(get_teachers_collection),
):
    try:
        teacher_model = TeacherModel.from_input(teacher)
    except ValidationError as e:
        print(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        ) from e

    try:
        saved_teacher = await teacher_repository.create_teacher(
            teacher_model,
            teachers_collection,
        )
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(e)}",
        )
    return saved_teacher.to_response_schema()


@router.get("/{teacher_id}", response_model=TeacherWithUserResponseSchema, tags=["teachers"])
async def get_teacher(teacher_id, collection=Depends(get_teachers_collection)):
    try:
        teacher = await teacher_repository.get_teacher_by_id(ObjectId(teacher_id), collection)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    return teacher.to_response_schema()

@router.patch("/{teacher_id}", response_model=TeacherWithUserResponseSchema)
async def update_teacher(teacher_id: str, 
                         update_data: TeacherUpdateSchema,
                         teachers_collection=Depends(get_teachers_collection)):
    update_dict = update_data.model_dump(exclude_none=True)
    
    updated_teacher = await teacher_repository.update_teacher_by_id(
            teacher_id,
            update_dict,
            teachers_collection
        )
    
    
    return updated_teacher.to_response_schema()


@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["teachers"])
async def delete_teacher(teacher_id: str, collection=Depends(get_teachers_collection)):
    try:
        await teacher_repository.delete_teacher_by_id(teacher_id, collection)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


