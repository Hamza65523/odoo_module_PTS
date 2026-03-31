"""Generic jsonPTS passthrough – gives access to ALL 211 PTS-2 commands."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_subject_or_api_key
from app.db.session import get_db
from app.schemas.device import PTSBatchRequest, PTSResponse, PTSSendRequest
from app.services.pts_client import PTSClient, PTSClientError

router = APIRouter(prefix="/pts", tags=["pts"])


@router.post("/send", response_model=PTSResponse)
async def pts_send(
    req: PTSSendRequest,
    _subject: str = Depends(get_subject_or_api_key),
    db: Session = Depends(get_db),
) -> PTSResponse:
    """Send a single jsonPTS request of any type.

    Examples::

        {"type": "GetDateTime", "data": {}}
        {"type": "PumpGetStatus", "data": {"Pump": 1}}
        {"type": "PumpSetPrices", "data": {"Pump": 1, "Prices": [1.25, 1.69]}}
        {"type": "GetFuelGradesPrices", "data": {}}
        {"type": "SetFuelGradesPrices", "data": {"FuelGradesPrices": [{"FuelGradeId": 1, "Price": 28.50}]}}
        {"type": "ProbeGetMeasurements", "data": {"Probe": 1}}
    """
    client = PTSClient()
    try:
        result = await client.send(req.type, req.data)
        return PTSResponse(
            protocol=result.get("Protocol", "jsonPTS"),
            packets=result.get("Packets", []),
        )
    except PTSClientError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        await client.close()


@router.post("/batch", response_model=PTSResponse)
async def pts_batch(
    req: PTSBatchRequest,
    _subject: str = Depends(get_subject_or_api_key),
    db: Session = Depends(get_db),
) -> PTSResponse:
    """Send multiple jsonPTS packets in a single request.

    Example (same as the curl from PTS web UI)::

        {
          "packets": [
            {"Id": 1, "Type": "PumpGetStatus", "Data": {"Pump": 1}},
            {"Id": 2, "Type": "PumpGetStatus", "Data": {"Pump": 2}},
            {"Id": 3, "Type": "GetDateTime",   "Data": {}},
            {"Id": 4, "Type": "GetFuelGradesPrices", "Data": {}}
          ]
        }
    """
    client = PTSClient()
    raw_packets = [
        {"Id": pkt.id, "Type": pkt.type, "Data": pkt.data}
        for pkt in req.packets
    ]
    try:
        result = await client.send("", packets=raw_packets, validate=False)
        return PTSResponse(
            protocol=result.get("Protocol", "jsonPTS"),
            packets=result.get("Packets", []),
        )
    except PTSClientError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        await client.close()
