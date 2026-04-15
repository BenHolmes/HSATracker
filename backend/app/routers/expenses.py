"""
Expense CRUD endpoints.

Pagination is handled by fastapi-pagination's paginate() helper, which
wraps the raw SQLAlchemy Select returned by build_expenses_query().
HsaPage raises the default page size to 50 and caps it at 1000, allowing
callers like the Track Reimbursement modal to fetch all OOP expenses in one
request without bypassing pagination entirely.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from fastapi_pagination import Page
from fastapi_pagination.customization import CustomizedPage, UseParamsFields
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.constants import HsaCategory, PaymentMethod
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
    category: HsaCategory | None = Query(None),
    payment_method: PaymentMethod | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """Return a paginated, optionally filtered list of expenses.

    Filters are ANDed together. Results are ordered by date DESC, then
    created_at DESC so the most recent entry wins on the same date.
    Invalid enum values for category or payment_method return 422.
    """
    query = crud.build_expenses_query(
        year=year,
        category=category.value if category else None,
        payment_method=payment_method.value if payment_method else None,
    )
    return await paginate(db, query)


@router.post("/", response_model=ExpenseOut, status_code=status.HTTP_201_CREATED)
async def create_expense(
    data: ExpenseCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new expense and return it with empty receipts and no reimbursement."""
    return await crud.create_expense(db, data)


@router.get("/years", response_model=list[int])
async def list_expense_years(db: AsyncSession = Depends(get_db)):
    """Return distinct calendar years that appear in the expenses table, newest first."""
    return await crud.get_expense_years(db)


@router.get("/{expense_id}", response_model=ExpenseOut)
async def get_expense(
    expense_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Fetch a single expense with its nested reimbursement and receipts."""
    return await crud.get_expense(db, expense_id)


@router.patch("/{expense_id}", response_model=ExpenseOut)
async def update_expense(
    expense_id: UUID,
    data: ExpenseUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Partially update an expense. Only fields present in the request body are changed."""
    return await crud.update_expense(db, expense_id, data)


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(
    expense_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete an expense. Cascades to its reimbursement record and all receipts."""
    await crud.delete_expense(db, expense_id)
