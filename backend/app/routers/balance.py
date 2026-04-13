from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.database import get_db
from app.schemas import BalanceCreate, BalanceList, BalanceOut

router = APIRouter()


@router.get("/", response_model=BalanceList)
async def list_balances(db: AsyncSession = Depends(get_db)):
    items, latest = await crud.get_balances(db)
    return BalanceList(items=items, latest=latest)


@router.post("/", response_model=BalanceOut, status_code=status.HTTP_201_CREATED)
async def create_balance(
    data: BalanceCreate,
    db: AsyncSession = Depends(get_db),
):
    return await crud.create_balance(db, data)


@router.delete("/{balance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_balance(
    balance_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    await crud.delete_balance(db, balance_id)
