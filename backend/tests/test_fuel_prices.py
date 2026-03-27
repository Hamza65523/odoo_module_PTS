from fastapi.testclient import TestClient

from app.main import app
from app.services.pts_client import PTSClient


def test_get_fuel_prices(monkeypatch):
    async def mock_send(self, packet_type, data=None):
        assert packet_type == "GetFuelGradesConfiguration"
        return {
            "Protocol": "jsonPTS",
            "Packets": [
                {
                    "Id": 1,
                    "Type": "FuelGradesConfiguration",
                    "Data": {
                        "FuelGrades": [
                            {"Id": 1, "Name": "Petrol", "Price": 10.5},
                            {"Id": 2, "Name": "Diesel", "Price": 9.7},
                            {"Id": 3, "Name": "LPG", "Price": 5.2},
                        ]
                    },
                }
            ],
        }

    monkeypatch.setattr(PTSClient, "send", mock_send)
    client = TestClient(app)
    response = client.get("/api/v1/fuel-prices", headers={"X-API-Key": "change_me_api_key"})
    assert response.status_code == 200
    body = response.json()
    assert len(body["items"]) >= 3


def test_update_fuel_prices(monkeypatch):
    async def mock_send(self, packet_type, data=None):
        assert packet_type == "SetFuelGradesPrices"
        return {"Protocol": "jsonPTS", "Packets": [{"Id": 1, "Type": "OK"}]}

    monkeypatch.setattr(PTSClient, "send", mock_send)
    client = TestClient(app)
    payload = {
        "items": [
            {"fuel_grade_id": 1, "name": "Petrol", "price": 11.1},
            {"fuel_grade_id": 2, "name": "Diesel", "price": 10.1},
            {"fuel_grade_id": 3, "name": "LPG", "price": 6.1},
        ]
    }
    response = client.put("/api/v1/fuel-prices", headers={"X-API-Key": "change_me_api_key"}, json=payload)
    assert response.status_code == 200
