from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead


class CalculationBase(BaseModel):
    operand1: float
    operand2: float
    operation: Literal["add", "sub", "mul", "div"]


class CalculationCreate(CalculationBase):
    pass


class CalculationUpdate(BaseModel):
    operand1: float | None = None
    operand2: float | None = None
    operation: Literal["add", "sub", "mul", "div"] | None = None


class CalculationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    operand1: float
    operand2: float
    operation: str
    result: float
    owner_id: int
    created_at: datetime
