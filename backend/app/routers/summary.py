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
    data = await crud.get_summary(db, year)
    return SummaryOut(**data)
