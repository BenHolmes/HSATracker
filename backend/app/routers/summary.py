"""
Dashboard summary endpoint.

Aggregates expenses, reimbursements, contributions, IRS limits, and the
latest account balance into a single response so the dashboard can be
rendered with one API call instead of five.
"""

from __future__ import annotations

import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.database import get_db
from app.schemas import SummaryOut

router = APIRouter()


@router.get("/", response_model=SummaryOut)
async def get_summary(
    year: int = Query(default_factory=lambda: datetime.date.today().year),
    db: AsyncSession = Depends(get_db),
):
    """Return aggregated statistics for a given tax year.

    All monetary totals are scoped to the requested year. Defaults to the
    current calendar year when no year is specified.
    """
    data = await crud.get_summary(db, year)
    return SummaryOut(**data)
