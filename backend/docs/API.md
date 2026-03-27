# API Documentation

Base path: `/api/v1`

## Authentication
- Endpoint: `POST /auth/token`
- Request:
```json
{"username":"admin","password":"admin"}
```
- Response:
```json
{"access_token":"...","token_type":"bearer"}
```

Use header:
- `Authorization: Bearer <token>`
- Optional hardening: `X-API-Key: <api_key>`

## Status
- `GET /status/backend`
- `GET /status/device`

## Monitoring
- `GET /pumps`
- `GET /probes`
- `GET /transactions`
- `GET /fuel-prices` (returns all configured fuel grades and prices)
- `PUT /fuel-prices` (updates prices by fuel grade id)

## Control Commands
- `POST /commands/{action}`

Actions:
- `pump_stop`
- `pump_emergency_stop`
- `pump_authorize`
- `pump_close_transaction`

Payload example:
```json
{"action":"pump_stop","payload":{"Pump":1}}
```

Fuel price update payload example:
```json
{
  "items": [
    {"fuel_grade_id": 1, "name": "Petrol", "price": 1.35},
    {"fuel_grade_id": 2, "name": "Diesel", "price": 1.29},
    {"fuel_grade_id": 3, "name": "LPG", "price": 0.79}
  ]
}
```

## Error Mapping
- HTTP errors are normalized by backend.
- PTS transport errors map to HTTP 400 with descriptive `detail`.
