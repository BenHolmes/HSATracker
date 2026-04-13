from __future__ import annotations

import datetime
from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.constants import CONTRIBUTION_LIMITS
from app.database import get_db
from app.schemas import ContributionCreate, ContributionOut, ContributionUpdate, PaginatedContributions

router = APIRouter()


@router.get("/", response_model=PaginatedContributions)
async def list_contributions(
    tax_year: int = Query(default_factory=lambda: datetime.date.today().year),
    db: AsyncSession = Depends(get_db),
):
    items, total_contributed = await crud.get_contributions(db, tax_year)

    limits = CONTRIBUTION_LIMITS.get(tax_year, CONTRIBUTION_LIMITS[max(CONTRIBUTION_LIMITS)])
    limit_individual = Decimal(limits[0])
    limit_family = Decimal(limits[1])

    return PaginatedContributions(
        items=items,
        total_contributed=total_contributed,
        tax_year=tax_year,
        limit_individual=limit_individual,
        limit_family=limit_family,
        remaining_individual=max(limit_individual - total_contributed, Decimal("0.00")),
        remaining_family=max(limit_family - total_contributed, Decimal("0.00")),
    )


@router.post("/", response_model=ContributionOut, status_code=status.HTTP_201_CREATED)
async def create_contribution(
    data: ContributionCreate,
    db: AsyncSession = Depends(get_db),
):
    return await crud.create_contribution(db, data)


@router.patch("/{contribution_id}", response_model=ContributionOut)
async def update_contribution(
    contribution_id: UUID,
    data: ContributionUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await crud.update_contribution(db, contribution_id, data)


@router.delete("/{contribution_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contribution(
    contribution_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    await crud.delete_contribution(db, contribution_id)
