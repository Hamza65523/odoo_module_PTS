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


class PumpPricesResponse(BaseModel):
    pump: int
    prices: list[float]
    user: str | None = None


class PumpSetPricesRequest(BaseModel):
    prices: list[float] = Field(
        ...,
        description="Array of prices for pump nozzles (up to 6), order matches nozzle order",
    )


# ---- Generic PTS passthrough ----------------------------------------

class PTSPacket(BaseModel):
    id: int = Field(default=1, alias="Id", description="Packet id (1-2147483647)")
    type: str = Field(..., alias="Type", description="jsonPTS request type, e.g. PumpGetStatus")
    data: dict = Field(default_factory=dict, alias="Data", description="Request-specific data")

    model_config = {"populate_by_name": True}


class PTSSendRequest(BaseModel):
    """Send a single jsonPTS packet."""
    type: str = Field(..., description="jsonPTS request type, e.g. GetDateTime, PumpSetPrices")
    data: dict = Field(default_factory=dict, description="Request-specific data payload")


class PTSBatchRequest(BaseModel):
    """Send multiple jsonPTS packets in one request (up to 600 tokens per PTS spec)."""
    packets: list[PTSPacket] = Field(
        ...,
        min_length=1,
        description="Array of jsonPTS packets to send in a single request",
    )


class PTSResponse(BaseModel):
    """Raw jsonPTS response with all packets."""
    protocol: str = "jsonPTS"
    packets: list[dict] = Field(default_factory=list)
