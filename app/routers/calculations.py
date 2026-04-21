from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_current_user, get_db

router = APIRouter(prefix="/calculations", tags=["calculations"])


def calculate_result(operand1: float, operand2: float, operation: str) -> float:
    if operation == "add":
        return operand1 + operand2
    if operation == "sub":
        return operand1 - operand2
    if operation == "mul":
        return operand1 * operand2
    if operation == "div":
        if operand2 == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Division by zero is not allowed")
        return operand1 / operand2
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported operation")


@router.get("", response_model=list[schemas.CalculationRead])
def browse_calculations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return db.query(models.Calculation).filter(models.Calculation.owner_id == current_user.id).all()


@router.get("/{calculation_id}", response_model=schemas.CalculationRead)
def read_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    calculation = (
        db.query(models.Calculation)
        .filter(models.Calculation.id == calculation_id, models.Calculation.owner_id == current_user.id)
        .first()
    )
    if calculation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calculation not found")
    return calculation


@router.post("", response_model=schemas.CalculationRead, status_code=status.HTTP_201_CREATED)
def add_calculation(
    payload: schemas.CalculationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    result = calculate_result(payload.operand1, payload.operand2, payload.operation)
    calculation = models.Calculation(
        operand1=payload.operand1,
        operand2=payload.operand2,
        operation=payload.operation,
        result=result,
        owner_id=current_user.id,
    )
    db.add(calculation)
    db.commit()
    db.refresh(calculation)
    return calculation


@router.put("/{calculation_id}", response_model=schemas.CalculationRead)
def edit_calculation(
    calculation_id: int,
    payload: schemas.CalculationUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    calculation = (
        db.query(models.Calculation)
        .filter(models.Calculation.id == calculation_id, models.Calculation.owner_id == current_user.id)
        .first()
    )
    if calculation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calculation not found")

    operand1 = payload.operand1 if payload.operand1 is not None else calculation.operand1
    operand2 = payload.operand2 if payload.operand2 is not None else calculation.operand2
    operation = payload.operation if payload.operation is not None else calculation.operation
    result = calculate_result(operand1, operand2, operation)

    calculation.operand1 = operand1
    calculation.operand2 = operand2
    calculation.operation = operation
    calculation.result = result
    db.commit()
    db.refresh(calculation)
    return calculation


@router.delete("/{calculation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    calculation = (
        db.query(models.Calculation)
        .filter(models.Calculation.id == calculation_id, models.Calculation.owner_id == current_user.id)
        .first()
    )
    if calculation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calculation not found")

    db.delete(calculation)
    db.commit()
    return None
