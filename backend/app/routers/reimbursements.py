"""
Reimbursement CRUD endpoints.

A reimbursement record ties an out-of-pocket expense to its repayment
lifecycle. Key business rules enforced in the CRUD layer:
  - Only expenses with payment_method='out_of_pocket' may be reimbursed.
  - Each expense may have at most one reimbursement record.
  - New records always start with status='pending'.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.database import get_db
from app.schemas import (
    PaginatedReimbursements,
    ReimbursementCreate,
    ReimbursementOut,
    ReimbursementUpdate,
)

router = APIRouter()


@router.get("/", response_model=PaginatedReimbursements)
async def list_reimbursements(
    status: str | None = Query(None),
    year: int | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(200, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    """Return reimbursements with aggregate totals and pagination.

    Optional filters:
      - status: 'pending' or 'reimbursed'
      - year: filters by the linked expense's date year
    The summary-card totals (pending_amount, reimbursed_amount_ytd) always
    reflect the full filtered set regardless of which page is requested.
    Default page size of 200 covers a full year of records in one request.
    """
    items, total, pending_amount, reimbursed_amount_ytd = await crud.get_reimbursements(
        db, status_filter=status, year=year, page=page, size=size
    )
    pages = max(1, -(total // -size))  # ceiling division without importing math
    return PaginatedReimbursements(
        items=items,
        total=total,
        page=page,
        pages=pages,
        pending_amount=pending_amount,
        reimbursed_amount_ytd=reimbursed_amount_ytd,
    )


@router.post("/", response_model=ReimbursementOut, status_code=status.HTTP_201_CREATED)
async def create_reimbursement(
    data: ReimbursementCreate,
    db: AsyncSession = Depends(get_db),
):
    """Start tracking an out-of-pocket expense for reimbursement.

    Returns 400 if the expense doesn't exist, isn't out-of-pocket,
    or already has a reimbursement record.
    """
    return await crud.create_reimbursement(db, data)


@router.patch("/{reimbursement_id}", response_model=ReimbursementOut)
async def update_reimbursement(
    reimbursement_id: UUID,
    data: ReimbursementUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update reimbursement status, amount, date, or notes.

    Typical usage: patch status to 'reimbursed' with reimbursed_date
    and reimbursed_amount once the HSA custodian has transferred funds.
    """
    return await crud.update_reimbursement(db, reimbursement_id, data)


@router.delete("/{reimbursement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reimbursement(
    reimbursement_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Remove a reimbursement record. The linked expense is not affected."""
    await crud.delete_reimbursement(db, reimbursement_id)
