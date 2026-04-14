from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from fastapi_pagination import Page
from fastapi_pagination.customization import CustomizedPage, UseParamsFields
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.database import get_db
from app.schemas import ExpenseCreate, ExpenseOut, ExpenseUpdate

router = APIRouter()

# Allow up to 1000 items per page so callers can fetch all results in one request
# (e.g. the "Track Reimbursement" modal which needs the full OOP expense list).
HsaPage = CustomizedPage[
    Page,
    UseParamsFields(size=Query(50, ge=1, le=1000)),
]


@router.get("/", response_model=HsaPage[ExpenseOut])
async def list_expenses(
    year: int | None = Query(None),
    category: str | None = Query(None),
    payment_method: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = crud.build_expenses_query(
        year=year,
        category=category,
        payment_method=payment_method,
    )
    return await paginate(db, query)


@router.post("/", response_model=ExpenseOut, status_code=status.HTTP_201_CREATED)
async def create_expense(
    data: ExpenseCreate,
    db: AsyncSession = Depends(get_db),
):
    return await crud.create_expense(db, data)


@router.get("/{expense_id}", response_model=ExpenseOut)
async def get_expense(
    expense_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    return await crud.get_expense(db, expense_id)


@router.patch("/{expense_id}", response_model=ExpenseOut)
async def update_expense(
    expense_id: UUID,
    data: ExpenseUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await crud.update_expense(db, expense_id, data)


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(
    expense_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    await crud.delete_expense(db, expense_id)
