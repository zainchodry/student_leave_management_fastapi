from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.department import Department

from app.schemas.department import (
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse
)

from app.utils.roles import (
    admin_required
)

router = APIRouter(
    prefix="/api/departments",
    tags=["Departments"]
)

@router.post(
    "/",
    response_model=DepartmentResponse
)
def create_department(

    payload: DepartmentCreate,

    current_user=Depends(
        admin_required
    ),

    db: Session = Depends(get_db)
):

    department = Department(
        **payload.model_dump()
    )

    db.add(department)

    db.commit()

    db.refresh(department)

    return department

@router.get(
    "/",
    response_model=list[DepartmentResponse]
)
def list_departments(

    db: Session = Depends(get_db)
):

    return db.query(
        Department
    ).all()

@router.put(
    "/{department_id}"
)
def update_department(

    department_id: int,

    payload: DepartmentUpdate,

    current_user=Depends(
        admin_required
    ),

    db: Session = Depends(get_db)
):

    department = db.query(
        Department
    ).filter(
        Department.id ==
        department_id
    ).first()

    if not department:

        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    for key, value in payload.model_dump(
        exclude_unset=True
    ).items():

        setattr(
            department,
            key,
            value
        )

    db.commit()

    return {
        "message":
        "Department updated"
    }

@router.delete(
    "/{department_id}"
)
def delete_department(

    department_id: int,

    current_user=Depends(
        admin_required
    ),

    db: Session = Depends(get_db)
):

    department = db.query(
        Department
    ).filter(
        Department.id ==
        department_id
    ).first()

    if not department:

        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    db.delete(department)

    db.commit()

    return {
        "message":
        "Department deleted"
    }