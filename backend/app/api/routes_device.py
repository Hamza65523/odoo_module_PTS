from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_subject_or_api_key
from app.db.session import get_db
from app.schemas.device import (
    CommandRequest,
    CommandResponse,
    FuelPricesResponse,
    FuelPricesUpdateRequest,
    ProbeResponse,
    PumpPricesResponse,
    PumpResponse,
    PumpSetPricesRequest,
    TransactionResponse,
)
from app.services.command_service import CommandService
from app.services.pts_client import PTSClient, PTSClientError
from app.services.status_service import StatusService

router = APIRouter(tags=["device"])


@router.get("/pumps", response_model=PumpResponse)
async def list_pumps(_subject: str = Depends(get_subject_or_api_key), db: Session = Depends(get_db)) -> PumpResponse:
    client = PTSClient()
    service = StatusService(db, client)
    try:
        items = await service.get_pumps()
        return PumpResponse(items=items)
    finally:
        await client.close()


@router.get("/probes", response_model=ProbeResponse)
async def list_probes(
    _subject: str = Depends(get_subject_or_api_key), db: Session = Depends(get_db)
) -> ProbeResponse:
    client = PTSClient()
    service = StatusService(db, client)
    try:
        items = await service.get_probes()
        return ProbeResponse(items=items)
    finally:
        await client.close()


@router.get("/transactions", response_model=TransactionResponse)
async def list_transactions(
    _subject: str = Depends(get_subject_or_api_key), db: Session = Depends(get_db)
) -> TransactionResponse:
    client = PTSClient()
    service = StatusService(db, client)
    try:
        items = await service.get_transactions()
        return TransactionResponse(items=items)
    finally:
        await client.close()


@router.post("/commands/{action}", response_model=CommandResponse)
async def run_command(
    action: str,
    req: CommandRequest,
    subject: str = Depends(get_subject_or_api_key),
    db: Session = Depends(get_db),
) -> CommandResponse:
    client = PTSClient()
    service = CommandService(db, client)
    try:
        result = await service.execute(action, req.payload, requested_by=subject)
    except (PTSClientError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        await client.close()
    return CommandResponse(status="ok", action=action, result=result)


@router.get("/fuel-prices", response_model=FuelPricesResponse)
async def get_fuel_prices(
    _subject: str = Depends(get_subject_or_api_key), db: Session = Depends(get_db)
) -> FuelPricesResponse:
    client = PTSClient()
    service = StatusService(db, client)
    try:
        fuel_grades = await service.get_fuel_grades()
        items = [
            {
                "fuel_grade_id": int(grade.get("Id", 0)),
                "name": grade.get("Name"),
                "price": float(grade.get("Price", 0.0)),
            }
            for grade in fuel_grades
            if grade.get("Id") is not None
        ]
        return FuelPricesResponse(items=items)
    finally:
        await client.close()


@router.put("/fuel-prices", response_model=CommandResponse)
async def update_fuel_prices(
    req: FuelPricesUpdateRequest,
    subject: str = Depends(get_subject_or_api_key),
    db: Session = Depends(get_db),
) -> CommandResponse:
    client = PTSClient()
    service = StatusService(db, client)
    try:
        pts_prices = [{"FuelGradeId": item.fuel_grade_id, "Price": item.price} for item in req.items]
        result = await service.set_fuel_grades_prices(pts_prices)
        return CommandResponse(status="ok", action="set_fuel_prices", result=result)
    except PTSClientError as exc:
        raise HTTPException(status_code=400, detail=f"Failed to update prices: {exc}") from exc
    finally:
        await client.close()


@router.get("/pumps/{pump_id}/prices", response_model=PumpPricesResponse)
async def get_pump_prices(
    pump_id: int,
    _subject: str = Depends(get_subject_or_api_key),
    db: Session = Depends(get_db),
) -> PumpPricesResponse:
    """Get current nozzle prices for a specific pump (PumpGetPrices → PumpPrices)."""
    client = PTSClient()
    service = StatusService(db, client)
    try:
        data = await service.pump_get_prices(pump_id)
        return PumpPricesResponse(
            pump=data.get("Pump", pump_id),
            prices=data.get("Prices", []),
            user=data.get("User"),
        )
    except PTSClientError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        await client.close()


@router.put("/pumps/{pump_id}/prices", response_model=CommandResponse)
async def set_pump_prices(
    pump_id: int,
    req: PumpSetPricesRequest,
    subject: str = Depends(get_subject_or_api_key),
    db: Session = Depends(get_db),
) -> CommandResponse:
    """Set nozzle prices for a specific pump (PumpSetPrices)."""
    client = PTSClient()
    service = StatusService(db, client)
    try:
        result = await service.pump_set_prices(pump_id, req.prices)
        return CommandResponse(status="ok", action="pump_set_prices", result=result)
    except PTSClientError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        await client.close()
