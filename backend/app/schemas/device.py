from pydantic import BaseModel, Field


class CommandRequest(BaseModel):
    action: str = Field(..., description="Supported action like pump_stop, pump_authorize")
    payload: dict = Field(default_factory=dict)


class CommandResponse(BaseModel):
    status: str
    action: str
    result: dict


class PumpResponse(BaseModel):
    items: list[dict]


class ProbeResponse(BaseModel):
    items: list[dict]


class TransactionResponse(BaseModel):
    items: list[dict]


class FuelGradePrice(BaseModel):
    fuel_grade_id: int
    name: str | None = None
    price: float


class FuelPricesResponse(BaseModel):
    items: list[FuelGradePrice]


class FuelPricesUpdateRequest(BaseModel):
    items: list[FuelGradePrice]
