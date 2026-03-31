# PTS-2 API Command Guide

**Base URL:** `http://localhost:8000/api/v1/commands/{CommandName}`  
**Method:** `POST`  
**Headers:**
```
X-API-Key: change_me_api_key
Content-Type: application/json
```

**Body format:**
```json
{"action": "CommandName", "payload": { ...data from PDF... }}
```

---

## Quick Examples

### Get petrol prices
```json
POST /api/v1/commands/GetFuelGradesPrices
{"action": "GetFuelGradesPrices", "payload": {}}
```

### Update petrol prices (by fuel grade)
```json
POST /api/v1/commands/SetFuelGradesPrices
{"action": "SetFuelGradesPrices", "payload": {"FuelGradesPrices": [{"FuelGradeId": 1, "Price": 2.80}, {"FuelGradeId": 2, "Price": 4.50}]}}
```

### Set prices on a specific pump
```json
POST /api/v1/commands/PumpSetPrices
{"action": "PumpSetPrices", "payload": {"Pump": 1, "Prices": [2.80, 4.50, 3.75]}}
```

### Get pump status
```json
POST /api/v1/commands/PumpGetStatus
{"action": "PumpGetStatus", "payload": {"Pump": 1}}
```

---

## GENERAL REQUESTS

| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 1 | `GetBatteryVoltage` | `{}` | Get battery voltage |
| 3 | `GetCpuTemperature` | `{}` | Get CPU temperature |
| 5 | `GetUniqueIdentifier` | `{}` | Get device unique ID |
| 7 | `GetControllerType` | `{}` | Get controller type |
| 9 | `GetFirmwareInformation` | `{}` | Get firmware version |
| 11 | `GetSdInformation` | `{}` | Get SD card info |
| 13 | `FileDelete` | `{"Name": "PtsLog.txt"}` | Delete a file from SD |
| 14 | `GetSystemOperationInformation` | `{}` | Get system operation info |
| 16 | `GetUserInformation` | `{}` | Get current user info |
| 18 | `GetTagInformation` | `{}` | Get tag info |
| 20 | `GetTagsTotalNumber` | `{}` | Get total number of tags |
| 22 | `GetLanguage` | `{}` | Get language setting |
| 24 | `GetMeasurementUnits` | `{}` | Get measurement units |
| 26 | `Restart` | `{}` | Restart controller |

---

## CONFIGURATION REQUESTS

### Date/Time
| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 29 | `GetDateTime` | `{}` | Get date and time |
| 30 | `SetDateTime` | `{"DateTime": "2026-03-31T12:00:00", "AutoSynchronize": true, "UTCOffset": 180}` | Set date and time |

### Network
| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 32 | `GetPtsNetworkSettings` | `{}` | Get network settings |
| 33 | `SetPtsNetworkSettings` | `{"IpAddress": [192,168,1,117], "NetMask": [255,255,255,0], "Gateway": [192,168,1,1], "HttpPort": 80, "HttpsPort": 443}` | Set network settings |

### System
| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 27 | `GetConfigurationIdentifier` | `{}` | Get config identifier |
| 38 | `GetDailyProcessingTime` | `{}` | Get daily processing time |
| 39 | `SetDailyProcessingTime` | `{"Hour": 0, "Minute": 0}` | Set daily processing time |
| 41 | `MakeDailyProcessing` | `{}` | Trigger daily processing |
| 42 | `GetSystemDecimalDigits` | `{}` | Get decimal digit settings |
| 43 | `SetSystemDecimalDigits` | `{"Price": 2, "Amount": 2, "Volume": 2, "AmountTotal": 2, "VolumeTotal": 2}` | Set decimal digits |

### Parameters
| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 45 | `GetParameter` | `{"Device": "Pump", "Number": 1, "Address": 1}` | Get parameter value |
| 46 | `SetParameter` | `{"Device": "Pump", "Number": 1, "Address": 1, "Value": "00000123"}` | Set parameter value |

### Fuel Grades & Prices
| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 54 | `GetFuelGradesPrices` | `{}` | **Get all fuel prices** |
| 55 | `SetFuelGradesPrices` | `{"FuelGradesPrices": [{"FuelGradeId": 1, "Price": 2.80}, {"FuelGradeId": 2, "Price": 4.50}]}` | **Set fuel prices** |
| 57 | `GetFuelGradesConfiguration` | `{}` | Get fuel grades config (names + prices) |
| 58 | `SetFuelGradesConfiguration` | See PDF section 58 | Set fuel grades config |
| 60 | `GetPricesSchedulerConfiguration` | `{}` | Get price scheduler config |
| 61 | `SetPricesSchedulerConfiguration` | See PDF section 61 | Set price scheduler |

### Pumps Configuration
| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 48 | `GetPumpsConfiguration` | `{}` | Get pumps config |
| 49 | `SetPumpsConfiguration` | See PDF section 49 | Set pumps config |
| 66 | `GetPumpNozzlesConfiguration` | `{}` | Get nozzle config |
| 67 | `SetPumpNozzlesConfiguration` | See PDF section 67 | Set nozzle config |

### Probes / Tanks
| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 51 | `GetProbesConfiguration` | `{}` | Get probes config |
| 52 | `SetProbesConfiguration` | See PDF section 52 | Set probes config |
| 69 | `GetTanksConfiguration` | `{}` | Get tanks config |
| 70 | `SetTanksConfiguration` | See PDF section 70 | Set tanks config |

### Price Boards
| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 72 | `GetPriceBoardsConfiguration` | `{}` | Get price boards config |
| 73 | `SetPriceBoardsConfiguration` | See PDF section 73 | Set price boards config |

### Readers
| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 75 | `GetReadersConfiguration` | `{}` | Get readers config |
| 76 | `SetReadersConfiguration` | See PDF section 76 | Set readers config |

### Users
| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 78 | `GetUsersConfiguration` | `{}` | Get users config |
| 79 | `SetUsersConfiguration` | See PDF section 79 | Set users config |
| 80 | `AddUserConfiguration` | See PDF section 80 | Add user |
| 81 | `EditUserConfiguration` | See PDF section 81 | Edit user |
| 82 | `DeleteUserConfiguration` | See PDF section 82 | Delete user |

### Payment Forms
| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 63 | `GetPaymentFormsConfiguration` | `{}` | Get payment forms |
| 64 | `SetPaymentFormsConfiguration` | See PDF section 64 | Set payment forms |

### Tags
| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 87 | `GetTagsList` | `{}` | Get all tags |
| 89 | `SetTagsList` | See PDF section 89 | Set tags list |
| 90 | `AddTagsToList` | See PDF section 90 | Add multiple tags |
| 91 | `AddTagToList` | See PDF section 91 | Add single tag |
| 92 | `EditTagInList` | See PDF section 92 | Edit tag |
| 93 | `DeleteTagFromList` | See PDF section 93 | Delete tag |

### Remote Server
| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 35 | `GetRemoteServerConfiguration` | `{}` | Get remote server config |
| 36 | `SetRemoteServerConfiguration` | See PDF section 36 | Set remote server config |

### Logging
| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 94 | `GetPortLoggingConfiguration` | `{}` | Get port logging config |
| 95 | `SetPortLoggingConfiguration` | See PDF section 95 | Set port logging |
| 97 | `GetRemoteServerLoggingConfiguration` | `{}` | Get remote server logging |
| 98 | `SetRemoteServerLoggingConfiguration` | See PDF section 98 | Set remote server logging |

### Backup / Records
| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 100 | `BackupConfiguration` | `{}` | Backup configuration |
| 101 | `RestoreConfiguration` | `{}` | Restore configuration |
| 102 | `GetUploadedRecordsInformation` | `{}` | Get uploaded records info |
| 104 | `SetUploadedRecordsNumber` | See PDF section 104 | Set uploaded records number |
| 105 | `ClearUploadedRecords` | `{"ClearPumpTransactions": true, "ClearTankMeasurements": false, "ClearInTankDeliveries": false, "ClearGpsRecords": false, "ClearAlertRecords": false, "ClearPayments": false, "ClearShifts": false}` | Clear uploaded records |

### Shifts / Ports
| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 106 | `GetShiftsOperation` | `{}` | Get shifts operation state |
| 107 | `SetShiftsOperation` | `{"Enabled": true}` | Enable/disable shifts |
| 109 | `GetPortsState` | `{}` | Get ports state |

---

## PUMPS CONTROL

### Status
| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 111 | `PumpGetStatus` | `{"Pump": 1}` | **Get pump status** (use Pump 0 for all pumps) |

### Prices
| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 129 | `PumpGetPrices` | `{"Pump": 1}` | **Get pump nozzle prices** |
| 130 | `PumpSetPrices` | `{"Pump": 1, "Prices": [2.80, 4.50, 3.75]}` | **Set pump nozzle prices** |

### Authorization & Transactions
| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 116 | `PumpAuthorize` | `{"Pump": 1, "Nozzle": 1, "Type": "Amount", "Dose": 50.00, "Price": 2.80}` | Authorize pump for filling |
| 118 | `PumpGetTransactionInformation` | `{"Pump": 1, "Transaction": 1}` | Get transaction info |
| 120 | `PumpStop` | `{"Pump": 1}` | Stop pump |
| 121 | `PumpEmergencyStop` | `{"Pump": 1}` | Emergency stop (use Pump 0 for all) |
| 122 | `PumpSuspend` | `{"Pump": 1}` | Suspend filling |
| 123 | `PumpResume` | `{"Pump": 1}` | Resume filling |
| 124 | `PumpCloseTransaction` | `{"Pump": 1}` | Close transaction |

### Totals
| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 125 | `PumpGetTotals` | `{"Pump": 1, "Nozzle": 1}` | Get nozzle totals |
| 127 | `PumpGetLastSavedTotals` | `{"Pump": 1}` | Get last saved totals |

### Display / Tags / Other
| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 132 | `PumpGetDisplayData` | `{"Pump": 1}` | Get pump display data |
| 134 | `PumpGetTag` | `{"Pump": 1}` | Get pump tag |
| 136 | `PumpGetAdditionalMeasurements` | `{"Pump": 1}` | Get additional measurements |
| 138 | `PumpLock` | `{"Pump": 1}` | Lock pump |
| 139 | `PumpUnlock` | `{"Pump": 1}` | Unlock pump |
| 140 | `PumpSetLights` | `{"Pump": 1}` | Set pump lights |
| 141 | `PumpGetAutomaticOperation` | `{"Pump": 1}` | Get automatic operation |
| 142 | `PumpSetAutomaticOperation` | `{"Pump": 1}` | Set automatic operation |

---

## PROBES (Tank Gauges)

| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 144 | `ProbeGetMeasurements` | `{"Probe": 1}` | **Get tank measurements** (use Probe 0 for all) |

---

## GPS

| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 166 | `GetGpsData` | `{}` | Get GPS data |

---

## PRICE BOARDS

| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 168 | `PriceBoardGetStatus` | `{"PriceBoard": 1}` | Get price board status |

---

## READERS

| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 170 | `ReaderGetTag` | `{"Reader": 1}` | Get reader tag |
| 172 | `ReaderGetStatus` | `{"Reader": 1}` | Get reader status |

---

## PAYMENTS

| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 174 | `PaymentCreateTransaction` | `{"Pump": 1, "Nozzle": 1, "Type": "Amount", "Dose": 50.00, "Price": 2.80}` | Create payment transaction |
| 176 | `PaymentGetTransactionInformation` | `{"Pump": 1, "Transaction": 1}` | Get payment transaction info |
| 178 | `PaymentRefundTransaction` | `{"Pump": 1, "Transaction": 1}` | Refund transaction |

---

## SHIFT MANAGEMENT

| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 179 | `ShiftOpen` | `{}` | Open shift |
| 181 | `ShiftClose` | `{}` | Close shift |
| 182 | `ShiftGetInformation` | `{}` | Get shift info |

---

## REPORTS

| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 184 | `ReportGetPumpTransactions` | `{"Pump": 1, "DateTimeStart": "2026-03-01T00:00:00", "DateTimeEnd": "2026-03-31T23:59:59"}` | Get pump transactions report |
| 186 | `ReportGetTankMeasurements` | `{"Probe": 1, "DateTimeStart": "2026-03-01T00:00:00", "DateTimeEnd": "2026-03-31T23:59:59"}` | Get tank measurements report |
| 188 | `ReportGetInTankDeliveries` | `{"Probe": 1, "DateTimeStart": "2026-03-01T00:00:00", "DateTimeEnd": "2026-03-31T23:59:59"}` | Get in-tank deliveries report |
| 190 | `ReportGetGpsRecords` | `{"DateTimeStart": "2026-03-01T00:00:00", "DateTimeEnd": "2026-03-31T23:59:59"}` | Get GPS records report |
| 192 | `ReportGetAlertRecords` | `{"DateTimeStart": "2026-03-01T00:00:00", "DateTimeEnd": "2026-03-31T23:59:59"}` | Get alert records report |
| 194 | `ReportGetPayments` | `{"DateTimeStart": "2026-03-01T00:00:00", "DateTimeEnd": "2026-03-31T23:59:59"}` | Get payments report |
| 196 | `ReportGetShifts` | `{"DateTimeStart": "2026-03-01T00:00:00", "DateTimeEnd": "2026-03-31T23:59:59"}` | Get shifts report |

---

## SELF-DIAGNOSTICS

| # | Command | Payload | Description |
|---|---------|---------|-------------|
| 198 | `MakeDiagnostics` | `{}` | Run diagnostics |

---

## COMMON USE CASES

### Get petrol price
```powershell
$body = '{"action":"GetFuelGradesPrices","payload":{}}'
Invoke-RestMethod -Uri http://localhost:8000/api/v1/commands/GetFuelGradesPrices -Method POST -Headers @{"X-API-Key"="change_me_api_key";"Content-Type"="application/json"} -Body $body | ConvertTo-Json -Depth 5
```

### Update petrol price (fuel grade 1 = Petrol, 2 = Diesel based on your device)
```powershell
$body = '{"action":"SetFuelGradesPrices","payload":{"FuelGradesPrices":[{"FuelGradeId":1,"Price":3.00},{"FuelGradeId":2,"Price":4.80}]}}'
Invoke-RestMethod -Uri http://localhost:8000/api/v1/commands/SetFuelGradesPrices -Method POST -Headers @{"X-API-Key"="change_me_api_key";"Content-Type"="application/json"} -Body $body | ConvertTo-Json -Depth 5
```

### Set prices on pump 1 (nozzle order: Petrol, Diesel, LPG)
```powershell
$body = '{"action":"PumpSetPrices","payload":{"Pump":1,"Prices":[2.80,4.50,3.75]}}'
Invoke-RestMethod -Uri http://localhost:8000/api/v1/commands/PumpSetPrices -Method POST -Headers @{"X-API-Key"="change_me_api_key";"Content-Type"="application/json"} -Body $body | ConvertTo-Json -Depth 5
```

### Get all pump statuses
```powershell
$body = '{"action":"PumpGetStatus","payload":{"Pump":0}}'
Invoke-RestMethod -Uri http://localhost:8000/api/v1/commands/PumpGetStatus -Method POST -Headers @{"X-API-Key"="change_me_api_key";"Content-Type"="application/json"} -Body $body | ConvertTo-Json -Depth 10
```

### Get tank level
```powershell
$body = '{"action":"ProbeGetMeasurements","payload":{"Probe":0}}'
Invoke-RestMethod -Uri http://localhost:8000/api/v1/commands/ProbeGetMeasurements -Method POST -Headers @{"X-API-Key"="change_me_api_key";"Content-Type"="application/json"} -Body $body | ConvertTo-Json -Depth 5
```

### Get fuel grades with names
```powershell
$body = '{"action":"GetFuelGradesConfiguration","payload":{}}'
Invoke-RestMethod -Uri http://localhost:8000/api/v1/commands/GetFuelGradesConfiguration -Method POST -Headers @{"X-API-Key"="change_me_api_key";"Content-Type"="application/json"} -Body $body | ConvertTo-Json -Depth 5
```

### Authorize pump for filling
```powershell
$body = '{"action":"PumpAuthorize","payload":{"Pump":1,"Nozzle":1,"Type":"Amount","Dose":50.00,"Price":2.80}}'
Invoke-RestMethod -Uri http://localhost:8000/api/v1/commands/PumpAuthorize -Method POST -Headers @{"X-API-Key"="change_me_api_key";"Content-Type"="application/json"} -Body $body | ConvertTo-Json -Depth 5
```

### Emergency stop all pumps
```powershell
$body = '{"action":"PumpEmergencyStop","payload":{"Pump":0}}'
Invoke-RestMethod -Uri http://localhost:8000/api/v1/commands/PumpEmergencyStop -Method POST -Headers @{"X-API-Key"="change_me_api_key";"Content-Type"="application/json"} -Body $body | ConvertTo-Json -Depth 5
```

### Get pump transactions report
```powershell
$body = '{"action":"ReportGetPumpTransactions","payload":{"Pump":0,"DateTimeStart":"2026-03-01T00:00:00","DateTimeEnd":"2026-03-31T23:59:59"}}'
Invoke-RestMethod -Uri http://localhost:8000/api/v1/commands/ReportGetPumpTransactions -Method POST -Headers @{"X-API-Key"="change_me_api_key";"Content-Type"="application/json"} -Body $body | ConvertTo-Json -Depth 10
```

---

## YOUR DEVICE INFO (from PTS response)

Based on your PTS device response:

| Fuel Grade ID | Name | Current Price |
|---|---|---|
| 1 | Petrol | 2.80 |
| 2 | Diesel | 4.50 |
| 3 | (LPG/Other) | 3.75 |

| Pump | Nozzles | Nozzle Prices |
|---|---|---|
| Pump 1 | 6 (3 active) | [2.80, 4.50, 3.75, 0, 0, 0] |
| Pump 2 | 6 (3 active) | [2.80, 4.50, 3.75, 0, 0, 0] |
| Pump 3 | 6 (3 active) | [3.75, 2.80, 4.50, 0, 0, 0] |
| Pump 4 | 6 (3 active) | [3.75, 2.80, 4.50, 0, 0, 0] |

---

## CURL EXAMPLES

```bash
# Get fuel prices
curl -X POST http://SERVER_IP:8000/api/v1/commands/GetFuelGradesPrices \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetFuelGradesPrices","payload":{}}'

# Update fuel prices
curl -X POST http://SERVER_IP:8000/api/v1/commands/SetFuelGradesPrices \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"SetFuelGradesPrices","payload":{"FuelGradesPrices":[{"FuelGradeId":1,"Price":3.00}]}}'

# Get pump status
curl -X POST http://SERVER_IP:8000/api/v1/commands/PumpGetStatus \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpGetStatus","payload":{"Pump":1}}'
```

Replace `SERVER_IP` with your server's IP address.

---

## NOTES

- **Python 3.10+** required
- **PTS_AUTH_MODE=digest** in `.env` (DIP switch 2 = OFF)
- **PTS_VERIFY_SSL=false** for self-signed certificate
- All commands are audited in the database
- Interactive API docs: `http://localhost:8000/docs`
- The `#` column references the PDF section number
