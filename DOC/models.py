"""
Pydantic v2 schemas for Smart Inventory & Stock Demand Forecasting System.
Source: PTM-05 D.1 OpenAPI + D.2 ERD.
"""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


Role = Literal["admin_gudang", "karyawan", "manajer"]
TransactionType = Literal["in", "out"]
BorrowingStatus = Literal["borrowed", "returned"]
DocumentType = Literal["receipt", "borrowing_evidence"]
DocumentStatus = Literal[
    "uploaded",
    "processing",
    "needs_verification",
    "verified",
    "rejected",
    "needs_manual_input",
    "failed",
]
ForecastPeriod = Literal["monthly"]
StockStatus = Literal["normal", "critical", "out_of_stock"]


class UserLoginRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role_id: int
    username: str
    role: Role


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["Bearer"]
    user: UserResponse


class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    description: str | None = None
    unit: str
    stock: float = Field(ge=0)
    minimum_stock: float = Field(ge=0)
    created_at: datetime
    updated_at: datetime


class CreateTransactionRequest(BaseModel):
    item_id: int = Field(ge=1)
    document_id: int | None = Field(default=None, ge=1)
    transaction_type: TransactionType
    quantity: float = Field(gt=0)
    transaction_date: datetime
    notes: str | None = None


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    item_id: int
    user_id: int
    document_id: int | None = None
    transaction_type: TransactionType
    quantity: float
    transaction_date: datetime
    notes: str | None = None
    verified: bool
    created_at: datetime
    updated_at: datetime


class CreateBorrowingRequest(BaseModel):
    item_id: int = Field(ge=1)
    borrower_id: int = Field(ge=1)
    quantity: float = Field(gt=0)
    borrowing_date: datetime
    expected_return_date: datetime | None = None
    notes: str | None = None


class BorrowingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    item_id: int
    borrower_id: int
    quantity: float
    status: BorrowingStatus
    borrowing_date: datetime
    expected_return_date: datetime | None = None
    returned_at: datetime | None = None
    notes: str | None = None
    created_at: datetime
    updated_at: datetime


class DocumentParseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    file_name: str
    file_path: str
    mime_type: str
    document_type: DocumentType
    status: DocumentStatus
    ocr_text: str | None = None
    extracted_data: dict[str, Any] | None = None
    confidence: float | None = Field(default=None, ge=0, le=1)
    verified_by: int | None = Field(default=None, ge=1)
    verified_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class VerificationRequest(BaseModel):
    status: Literal["verified", "rejected"]
    extracted_data: dict[str, Any] | None = None


class ForecastRequest(BaseModel):
    item_id: int = Field(ge=1)
    forecast_period: ForecastPeriod


class ForecastResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    item_id: int
    forecast_period: ForecastPeriod
    forecast_value: float
    reorder_point: float
    current_stock: float
    stock_status: StockStatus
    model_name: str | None = None
    model_accuracy: float | None = Field(default=None, ge=0, le=1)
    processed_at: datetime
    created_at: datetime
    updated_at: datetime


class ErrorResponse(BaseModel):
    error: str
    message: str
    details: dict[str, Any] | None = None
