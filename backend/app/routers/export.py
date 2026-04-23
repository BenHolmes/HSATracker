"""
Data export endpoints.

GET /api/v1/export/expenses.csv  — all expenses (or a single year) as CSV
GET /api/v1/export/full.zip      — ZIP with expenses.csv + receipt files
                                   renamed to YYYY-MM-DD_provider_original.ext

Both endpoints accept an optional ?year= query parameter. Omitting it exports
everything in the database.

Receipt files that are present in the database but missing from disk (e.g. the
upload volume was wiped) are silently skipped in the ZIP so the rest of the
archive is still usable.
"""

import csv
import io
import os
import re
import zipfile
from pathlib import Path

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Expense

router = APIRouter()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _upload_dir() -> Path:
    return Path(os.environ.get("UPLOAD_DIR", "/app/uploads"))


def _sanitize(text: str) -> str:
    """Collapse any non-alphanumeric character run to a single underscore."""
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def _unique_arc_name(date_str: str, provider: str, original: str, used: set[str]) -> str:
    """Return a collision-free archive path for a receipt inside the ZIP.

    Format: receipts/YYYY-MM-DD_provider_stem.ext
    If the name is already taken (same date + provider + filename), a numeric
    suffix is appended before the extension.
    """
    # Split extension on the last dot so stems like "scan.2024.01" stay intact
    if "." in original:
        stem, ext = original.rsplit(".", 1)
        ext = f".{ext}"
    else:
        stem, ext = original, ""

    base = f"receipts/{date_str}_{_sanitize(provider)}_{_sanitize(stem)}{ext}"
    if base not in used:
        used.add(base)
        return base

    counter = 2
    while True:
        candidate = f"receipts/{date_str}_{_sanitize(provider)}_{_sanitize(stem)}_{counter}{ext}"
        if candidate not in used:
            used.add(candidate)
            return candidate
        counter += 1


def _label(value: str) -> str:
    """Convert snake_case enum values to Title Case for human-readable CSV output."""
    return value.replace("_", " ").title()


async def _fetch_expenses(db: AsyncSession, year: int | None) -> list[Expense]:
    """Load all expenses with eager-loaded receipts and reimbursements."""
    query = (
        select(Expense)
        .options(
            selectinload(Expense.reimbursement),
            selectinload(Expense.receipts),
        )
        .order_by(Expense.date.desc(), Expense.created_at.desc())
    )
    if year is not None:
        query = query.where(extract("year", Expense.date) == year)
    result = await db.execute(query)
    return list(result.scalars().all())


def _build_csv(expenses: list[Expense]) -> bytes:
    """Serialize expenses to a UTF-8 CSV with BOM (Excel-compatible)."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow([
        "Date",
        "Provider",
        "Description",
        "Category",
        "Payment Method",
        "Amount",
        "Notes",
        "Reimbursement Status",
        "Reimbursed Amount",
        "Reimbursed Date",
    ])
    for e in expenses:
        r = e.reimbursement
        writer.writerow([
            str(e.date),
            e.provider_name,
            e.description,
            _label(e.category),
            _label(e.payment_method),
            f"{e.amount:.2f}",
            e.notes or "",
            r.status if r else "",
            f"{r.reimbursed_amount:.2f}" if (r and r.reimbursed_amount is not None) else "",
            str(r.reimbursed_date) if (r and r.reimbursed_date) else "",
        ])
    # utf-8-sig writes a BOM so Excel opens the file with the correct encoding
    return buf.getvalue().encode("utf-8-sig")


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/expenses.csv", summary="Export expenses as CSV")
async def export_csv(
    year: int | None = Query(None, description="Filter by calendar year; omit for all years"),
    db: AsyncSession = Depends(get_db),
):
    """Download all expenses (optionally filtered by year) as a CSV file."""
    expenses = await _fetch_expenses(db, year)
    content = _build_csv(expenses)
    filename = f"expenses_{year}.csv" if year else "expenses.csv"
    return StreamingResponse(
        io.BytesIO(content),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/full.zip", summary="Export expenses + receipts as ZIP")
async def export_zip(
    year: int | None = Query(None, description="Filter by calendar year; omit for all years"),
    db: AsyncSession = Depends(get_db),
):
    """Download a ZIP archive containing expenses.csv and all receipt files.

    Receipt files are renamed to YYYY-MM-DD_provider_originalname.ext so they
    are immediately identifiable. Files missing from disk are silently skipped.
    """
    expenses = await _fetch_expenses(db, year)
    upload_dir = _upload_dir()

    buf = io.BytesIO()
    used_names: set[str] = set()

    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("expenses.csv", _build_csv(expenses))

        for expense in expenses:
            date_str = str(expense.date)  # YYYY-MM-DD
            for receipt in expense.receipts:
                file_path = upload_dir / receipt.storage_path
                if not file_path.exists():
                    continue
                arc_name = _unique_arc_name(
                    date_str, expense.provider_name, receipt.original_filename, used_names
                )
                zf.write(str(file_path), arcname=arc_name)

    buf.seek(0)
    filename = f"hsatracker_{year}.zip" if year else "hsatracker_export.zip"
    return StreamingResponse(
        buf,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
