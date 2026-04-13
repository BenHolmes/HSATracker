from __future__ import annotations

import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


# ---------------------------------------------------------------------------
# Receipts (nested in ExpenseOut)
# ---------------------------------------------------------------------------

class ReceiptOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    expense_id: UUID
    original_filename: str
    mime_type: str
    file_size: int
    created_at: datetime.datetime


# ---------------------------------------------------------------------------
# Reimbursements
# ---------------------------------------------------------------------------

class ReimbursementSummary(BaseModel):
    """Nested inside ExpenseOut — lightweight view of reimbursement status."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: str
    reimbursed_date: datetime.date | None
    reimbursed_amount: Decimal | None


class ReimbursementCreate(BaseModel):
    expense_id: UUID
    notes: str | None = None


class ReimbursementUpdate(BaseModel):
    status: str | None = None
    reimbursed_date: datetime.date | None = None
    reimbursed_amount: Decimal | None = None
    notes: str | None = None


class ExpenseSummary(BaseModel):
    """Nested inside ReimbursementOut — lightweight view of the linked expense."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    date: datetime.date
    provider_name: str
    amount: Decimal


class ReimbursementOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    expense_id: UUID
    expense: ExpenseSummary
    status: str
    reimbursed_date: datetime.date | None
    reimbursed_amount: Decimal | None
    notes: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime


class PaginatedReimbursements(BaseModel):
    items: list[ReimbursementOut]
    total: int
    pending_amount: Decimal
    reimbursed_amount_ytd: Decimal


# ---------------------------------------------------------------------------
# Expenses
# ---------------------------------------------------------------------------

class ExpenseCreate(BaseModel):
    date: datetime.date
    provider_name: str
    description: str
    amount: Decimal
    category: str
    payment_method: str
    notes: str | None = None


class ExpenseUpdate(BaseModel):
    date: datetime.date | None = None
    provider_name: str | None = None
    description: str | None = None
    amount: Decimal | None = None
    category: str | None = None
    payment_method: str | None = None
    notes: str | None = None


class ExpenseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    date: datetime.date
    provider_name: str
    description: str
    amount: Decimal
    category: str
    payment_method: str
    notes: str | None
    reimbursement: ReimbursementSummary | None
    receipts: list[ReceiptOut]
    created_at: datetime.datetime
    updated_at: datetime.datetime


class PaginatedExpenses(BaseModel):
    items: list[ExpenseOut]
    total: int


# ---------------------------------------------------------------------------
# Contributions
# ---------------------------------------------------------------------------

class ContributionCreate(BaseModel):
    date: datetime.date
    amount: Decimal
    source: str
    tax_year: int
    notes: str | None = None


class ContributionUpdate(BaseModel):
    date: datetime.date | None = None
    amount: Decimal | None = None
    source: str | None = None
    tax_year: int | None = None
    notes: str | None = None


class ContributionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    date: datetime.date
    amount: Decimal
    source: str
    tax_year: int
    notes: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime


class PaginatedContributions(BaseModel):
    items: list[ContributionOut]
    total_contributed: Decimal
    tax_year: int
    limit_individual: Decimal
    limit_family: Decimal
    remaining_individual: Decimal
    remaining_family: Decimal


# ---------------------------------------------------------------------------
# Account Balance
# ---------------------------------------------------------------------------

class BalanceCreate(BaseModel):
    balance: Decimal
    as_of_date: datetime.date
    notes: str | None = None


class BalanceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    balance: Decimal
    as_of_date: datetime.date
    notes: str | None
    created_at: datetime.datetime


class BalanceList(BaseModel):
    items: list[BalanceOut]
    latest: BalanceOut | None


# ---------------------------------------------------------------------------
# Summary (dashboard)
# ---------------------------------------------------------------------------

class SummaryOut(BaseModel):
    year: int
    total_expenses: Decimal
    hsa_paid_expenses: Decimal
    out_of_pocket_expenses: Decimal
    pending_reimbursement: Decimal
    reimbursed_ytd: Decimal
    total_contributed: Decimal
    limit_individual: Decimal
    limit_family: Decimal
    remaining_individual: Decimal
    remaining_family: Decimal
    latest_balance: Decimal | None
    latest_balance_date: datetime.date | None
