# PTS-2 API Command Guide

## How It Works

Every command in the PTS-2 PDF can be sent through a single endpoint on your backend.

**Endpoint:** `POST http://localhost:8000/api/v1/commands/{CommandName}`

**Headers:**
```
X-API-Key: change_me_api_key
Content-Type: application/json
```

**Body:**
```json
{"action": "CommandName", "payload": { ... }}
```

### How to read the PDF and build your request

The PDF shows jsonPTS packets like this:

```json
{
  "Protocol": "jsonPTS",
  "Packets": [{
    "Id": 1,
    "Type": "PumpSetPrices",
    "Data": { "Pump": 1, "Prices": [1.25, 1.69, 1.33] }
  }]
}
```

You only need two pieces:

| PDF field | Your API field | What it is |
|-----------|---------------|------------|
| `"Type"`  | `"action"` | The command name (e.g. `PumpSetPrices`, `GetDateTime`) |
| `"Data"`  | `"payload"` | The parameters for that command |

The backend handles `Protocol`, `Packets`, `Id`, authentication, and everything else automatically.

---

## Quick Reference — Common Tasks

### Get petrol / fuel prices

```bash
curl -X POST http://localhost:8000/api/v1/commands/GetFuelGradesPrices \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetFuelGradesPrices","payload":{}}'
```

### Update fuel prices globally

```bash
curl -X POST http://localhost:8000/api/v1/commands/SetFuelGradesPrices \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"SetFuelGradesPrices","payload":{"FuelGradesPrices":[{"FuelGradeId":1,"Price":3.00},{"FuelGradeId":2,"Price":4.80},{"FuelGradeId":3,"Price":3.75}]}}'
```

### Set prices on a specific pump

```bash
curl -X POST http://localhost:8000/api/v1/commands/PumpSetPrices \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpSetPrices","payload":{"Pump":1,"Prices":[2.80,4.50,3.75]}}'
```

### Get pump status (single pump)

```bash
curl -X POST http://localhost:8000/api/v1/commands/PumpGetStatus \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpGetStatus","payload":{"Pump":1}}'
```

### Get all pumps status

```bash
curl -X POST http://localhost:8000/api/v1/commands/PumpGetStatus \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpGetStatus","payload":{"Pump":0}}'
```

### Get date/time

```bash
curl -X POST http://localhost:8000/api/v1/commands/GetDateTime \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetDateTime","payload":{}}'
```

---

## All Commands by Category

Every curl command below follows the same pattern. Replace `SERVER` with `localhost` or your server IP.

```
curl -X POST http://SERVER:8000/api/v1/commands/COMMAND_NAME \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"COMMAND_NAME","payload":PAYLOAD}'
```

---

### 1. GENERAL

#### Get Battery Voltage (PDF #1)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetBatteryVoltage \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetBatteryVoltage","payload":{}}'
```

#### Get CPU Temperature (PDF #3)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetCpuTemperature \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetCpuTemperature","payload":{}}'
```

#### Get Unique Identifier (PDF #5)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetUniqueIdentifier \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetUniqueIdentifier","payload":{}}'
```

#### Get Controller Type (PDF #7)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetControllerType \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetControllerType","payload":{}}'
```

#### Get Firmware Information (PDF #9)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetFirmwareInformation \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetFirmwareInformation","payload":{}}'
```

#### Get SD Card Information (PDF #11)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetSdInformation \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetSdInformation","payload":{}}'
```

#### Delete File from SD (PDF #13)
```bash
curl -X POST http://localhost:8000/api/v1/commands/FileDelete \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"FileDelete","payload":{"Name":"PtsLog.txt"}}'
```

#### Get System Operation Information (PDF #14)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetSystemOperationInformation \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetSystemOperationInformation","payload":{}}'
```

#### Get User Information (PDF #16)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetUserInformation \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetUserInformation","payload":{}}'
```

#### Get Tag Information (PDF #18)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetTagInformation \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetTagInformation","payload":{}}'
```

#### Get Tags Total Number (PDF #20)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetTagsTotalNumber \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetTagsTotalNumber","payload":{}}'
```

#### Get Language (PDF #22)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetLanguage \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetLanguage","payload":{}}'
```

#### Get Measurement Units (PDF #24)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetMeasurementUnits \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetMeasurementUnits","payload":{}}'
```

#### Restart Controller (PDF #26)
```bash
curl -X POST http://localhost:8000/api/v1/commands/Restart \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"Restart","payload":{}}'
```

---

### 2. DATE & TIME

#### Get Date/Time (PDF #29)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetDateTime \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetDateTime","payload":{}}'
```

#### Set Date/Time (PDF #30)
```bash
curl -X POST http://localhost:8000/api/v1/commands/SetDateTime \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"SetDateTime","payload":{"DateTime":"2026-03-31T12:00:00","AutoSynchronize":true,"UTCOffset":180}}'
```

---

### 3. CONFIGURATION

#### Get Configuration Identifier (PDF #27)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetConfigurationIdentifier \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetConfigurationIdentifier","payload":{}}'
```

#### Get Network Settings (PDF #32)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetPtsNetworkSettings \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetPtsNetworkSettings","payload":{}}'
```

#### Set Network Settings (PDF #33)
```bash
curl -X POST http://localhost:8000/api/v1/commands/SetPtsNetworkSettings \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"SetPtsNetworkSettings","payload":{"IpAddress":[192,168,1,117],"NetMask":[255,255,255,0],"Gateway":[192,168,1,1],"HttpPort":80,"HttpsPort":443}}'
```

#### Get Remote Server Configuration (PDF #35)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetRemoteServerConfiguration \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetRemoteServerConfiguration","payload":{}}'
```

#### Set Remote Server Configuration (PDF #36)
```bash
curl -X POST http://localhost:8000/api/v1/commands/SetRemoteServerConfiguration \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"SetRemoteServerConfiguration","payload":{"IpAddress":[192,168,1,100],"Port":8080,"Enabled":true}}'
```

#### Get Daily Processing Time (PDF #38)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetDailyProcessingTime \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetDailyProcessingTime","payload":{}}'
```

#### Set Daily Processing Time (PDF #39)
```bash
curl -X POST http://localhost:8000/api/v1/commands/SetDailyProcessingTime \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"SetDailyProcessingTime","payload":{"Hour":0,"Minute":0}}'
```

#### Make Daily Processing (PDF #41)
```bash
curl -X POST http://localhost:8000/api/v1/commands/MakeDailyProcessing \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"MakeDailyProcessing","payload":{}}'
```

#### Get System Decimal Digits (PDF #42)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetSystemDecimalDigits \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetSystemDecimalDigits","payload":{}}'
```

#### Set System Decimal Digits (PDF #43)
```bash
curl -X POST http://localhost:8000/api/v1/commands/SetSystemDecimalDigits \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"SetSystemDecimalDigits","payload":{"Price":2,"Amount":2,"Volume":2,"AmountTotal":2,"VolumeTotal":2}}'
```

#### Get Parameter (PDF #45)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetParameter \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetParameter","payload":{"Device":"Pump","Number":1,"Address":1}}'
```

#### Set Parameter (PDF #46)
```bash
curl -X POST http://localhost:8000/api/v1/commands/SetParameter \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"SetParameter","payload":{"Device":"Pump","Number":1,"Address":1,"Value":"00000123"}}'
```

---

### 4. FUEL GRADES & PRICES

#### Get Fuel Grades Prices (PDF #54)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetFuelGradesPrices \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetFuelGradesPrices","payload":{}}'
```

#### Set Fuel Grades Prices (PDF #55)
Payload: `FuelGradesPrices` = array of `{"FuelGradeId": N, "Price": X.XX}`
```bash
curl -X POST http://localhost:8000/api/v1/commands/SetFuelGradesPrices \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"SetFuelGradesPrices","payload":{"FuelGradesPrices":[{"FuelGradeId":1,"Price":2.80},{"FuelGradeId":2,"Price":4.50},{"FuelGradeId":3,"Price":3.75}]}}'
```

#### Get Fuel Grades Configuration (PDF #57)
Returns fuel grade names, IDs, and prices.
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetFuelGradesConfiguration \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetFuelGradesConfiguration","payload":{}}'
```

#### Set Fuel Grades Configuration (PDF #58)
```bash
curl -X POST http://localhost:8000/api/v1/commands/SetFuelGradesConfiguration \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"SetFuelGradesConfiguration","payload":{"FuelGrades":[{"Id":1,"Name":"Petrol","Price":2.80},{"Id":2,"Name":"Diesel","Price":4.50},{"Id":3,"Name":"LPG","Price":3.75}]}}'
```

#### Get Prices Scheduler Configuration (PDF #60)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetPricesSchedulerConfiguration \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetPricesSchedulerConfiguration","payload":{}}'
```

---

### 5. PUMPS CONFIGURATION

#### Get Pumps Configuration (PDF #48)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetPumpsConfiguration \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetPumpsConfiguration","payload":{}}'
```

#### Get Pump Nozzles Configuration (PDF #66)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetPumpNozzlesConfiguration \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetPumpNozzlesConfiguration","payload":{}}'
```

---

### 6. PROBES & TANKS CONFIGURATION

#### Get Probes Configuration (PDF #51)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetProbesConfiguration \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetProbesConfiguration","payload":{}}'
```

#### Get Tanks Configuration (PDF #69)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetTanksConfiguration \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetTanksConfiguration","payload":{}}'
```

---

### 7. PAYMENT FORMS

#### Get Payment Forms Configuration (PDF #63)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetPaymentFormsConfiguration \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetPaymentFormsConfiguration","payload":{}}'
```

---

### 8. PRICE BOARDS

#### Get Price Boards Configuration (PDF #72)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetPriceBoardsConfiguration \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetPriceBoardsConfiguration","payload":{}}'
```

---

### 9. READERS

#### Get Readers Configuration (PDF #75)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetReadersConfiguration \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetReadersConfiguration","payload":{}}'
```

---

### 10. USERS

#### Get Users Configuration (PDF #78)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetUsersConfiguration \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetUsersConfiguration","payload":{}}'
```

#### Add User (PDF #80)
```bash
curl -X POST http://localhost:8000/api/v1/commands/AddUserConfiguration \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"AddUserConfiguration","payload":{"Name":"operator1","Password":"1234","Permission":"Control"}}'
```

#### Edit User (PDF #81)
```bash
curl -X POST http://localhost:8000/api/v1/commands/EditUserConfiguration \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"EditUserConfiguration","payload":{"Name":"operator1","Password":"5678","Permission":"Control"}}'
```

#### Delete User (PDF #82)
```bash
curl -X POST http://localhost:8000/api/v1/commands/DeleteUserConfiguration \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"DeleteUserConfiguration","payload":{"Name":"operator1"}}'
```

---

### 11. TAGS

#### Get Tags List (PDF #87)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetTagsList \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetTagsList","payload":{}}'
```

#### Add Tag to List (PDF #91)
```bash
curl -X POST http://localhost:8000/api/v1/commands/AddTagToList \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"AddTagToList","payload":{"Tag":"ABCDEF01","Type":"Mifare"}}'
```

#### Edit Tag in List (PDF #92)
```bash
curl -X POST http://localhost:8000/api/v1/commands/EditTagInList \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"EditTagInList","payload":{"Tag":"ABCDEF01","Type":"Mifare"}}'
```

#### Delete Tag from List (PDF #93)
```bash
curl -X POST http://localhost:8000/api/v1/commands/DeleteTagFromList \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"DeleteTagFromList","payload":{"Tag":"ABCDEF01"}}'
```

---

### 12. LOGGING

#### Get Port Logging Configuration (PDF #94)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetPortLoggingConfiguration \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetPortLoggingConfiguration","payload":{}}'
```

#### Get Remote Server Logging Configuration (PDF #97)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetRemoteServerLoggingConfiguration \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetRemoteServerLoggingConfiguration","payload":{}}'
```

---

### 13. BACKUP & RECORDS

#### Backup Configuration (PDF #100)
```bash
curl -X POST http://localhost:8000/api/v1/commands/BackupConfiguration \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"BackupConfiguration","payload":{}}'
```

#### Restore Configuration (PDF #101)
```bash
curl -X POST http://localhost:8000/api/v1/commands/RestoreConfiguration \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"RestoreConfiguration","payload":{}}'
```

#### Get Uploaded Records Information (PDF #102)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetUploadedRecordsInformation \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetUploadedRecordsInformation","payload":{}}'
```

#### Clear Uploaded Records (PDF #105)
```bash
curl -X POST http://localhost:8000/api/v1/commands/ClearUploadedRecords \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"ClearUploadedRecords","payload":{"ClearPumpTransactions":true,"ClearTankMeasurements":false,"ClearInTankDeliveries":false,"ClearGpsRecords":false,"ClearAlertRecords":false,"ClearPayments":false,"ClearShifts":false}}'
```

---

### 14. SHIFTS & PORTS

#### Get Shifts Operation (PDF #106)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetShiftsOperation \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetShiftsOperation","payload":{}}'
```

#### Set Shifts Operation (PDF #107)
```bash
curl -X POST http://localhost:8000/api/v1/commands/SetShiftsOperation \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"SetShiftsOperation","payload":{"Enabled":true}}'
```

#### Get Ports State (PDF #109)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetPortsState \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetPortsState","payload":{}}'
```

---

### 15. PUMP CONTROL

#### Get Pump Status (PDF #111)
Use `"Pump": 0` to get all pumps at once.
```bash
curl -X POST http://localhost:8000/api/v1/commands/PumpGetStatus \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpGetStatus","payload":{"Pump":1}}'
```

#### Authorize Pump (PDF #116)
Types: `"FullTank"`, `"Amount"`, `"Volume"`
```bash
curl -X POST http://localhost:8000/api/v1/commands/PumpAuthorize \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpAuthorize","payload":{"Pump":1,"Nozzle":1,"Type":"Amount","Dose":50.00,"Price":2.80}}'
```

#### Get Transaction Information (PDF #118)
```bash
curl -X POST http://localhost:8000/api/v1/commands/PumpGetTransactionInformation \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpGetTransactionInformation","payload":{"Pump":1,"Transaction":1}}'
```

#### Stop Pump (PDF #120)
```bash
curl -X POST http://localhost:8000/api/v1/commands/PumpStop \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpStop","payload":{"Pump":1}}'
```

#### Emergency Stop (PDF #121)
Use `"Pump": 0` to stop all pumps.
```bash
curl -X POST http://localhost:8000/api/v1/commands/PumpEmergencyStop \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpEmergencyStop","payload":{"Pump":0}}'
```

#### Suspend Filling (PDF #122)
```bash
curl -X POST http://localhost:8000/api/v1/commands/PumpSuspend \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpSuspend","payload":{"Pump":1}}'
```

#### Resume Filling (PDF #123)
```bash
curl -X POST http://localhost:8000/api/v1/commands/PumpResume \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpResume","payload":{"Pump":1}}'
```

#### Close Transaction (PDF #124)
```bash
curl -X POST http://localhost:8000/api/v1/commands/PumpCloseTransaction \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpCloseTransaction","payload":{"Pump":1}}'
```

#### Get Pump Totals (PDF #125)
```bash
curl -X POST http://localhost:8000/api/v1/commands/PumpGetTotals \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpGetTotals","payload":{"Pump":1,"Nozzle":1}}'
```

#### Get Last Saved Totals (PDF #127)
```bash
curl -X POST http://localhost:8000/api/v1/commands/PumpGetLastSavedTotals \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpGetLastSavedTotals","payload":{"Pump":1}}'
```

#### Get Pump Prices (PDF #129)
```bash
curl -X POST http://localhost:8000/api/v1/commands/PumpGetPrices \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpGetPrices","payload":{"Pump":1}}'
```

#### Set Pump Prices (PDF #130)
Array order = nozzle order (up to 6 nozzles).
```bash
curl -X POST http://localhost:8000/api/v1/commands/PumpSetPrices \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpSetPrices","payload":{"Pump":1,"Prices":[2.80,4.50,3.75,0,0,0]}}'
```

#### Get Pump Display Data (PDF #132)
```bash
curl -X POST http://localhost:8000/api/v1/commands/PumpGetDisplayData \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpGetDisplayData","payload":{"Pump":1}}'
```

#### Get Pump Tag (PDF #134)
```bash
curl -X POST http://localhost:8000/api/v1/commands/PumpGetTag \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpGetTag","payload":{"Pump":1}}'
```

#### Get Additional Measurements (PDF #136)
```bash
curl -X POST http://localhost:8000/api/v1/commands/PumpGetAdditionalMeasurements \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpGetAdditionalMeasurements","payload":{"Pump":1}}'
```

#### Lock Pump (PDF #138)
```bash
curl -X POST http://localhost:8000/api/v1/commands/PumpLock \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpLock","payload":{"Pump":1}}'
```

#### Unlock Pump (PDF #139)
```bash
curl -X POST http://localhost:8000/api/v1/commands/PumpUnlock \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpUnlock","payload":{"Pump":1}}'
```

#### Set Pump Lights (PDF #140)
```bash
curl -X POST http://localhost:8000/api/v1/commands/PumpSetLights \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpSetLights","payload":{"Pump":1}}'
```

#### Get Automatic Operation (PDF #141)
```bash
curl -X POST http://localhost:8000/api/v1/commands/PumpGetAutomaticOperation \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpGetAutomaticOperation","payload":{"Pump":1}}'
```

#### Set Automatic Operation (PDF #142)
```bash
curl -X POST http://localhost:8000/api/v1/commands/PumpSetAutomaticOperation \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PumpSetAutomaticOperation","payload":{"Pump":1}}'
```

---

### 16. PROBES (Tank Gauges)

#### Get Probe Measurements (PDF #144)
Use `"Probe": 0` to get all probes.
```bash
curl -X POST http://localhost:8000/api/v1/commands/ProbeGetMeasurements \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"ProbeGetMeasurements","payload":{"Probe":1}}'
```

---

### 17. GPS

#### Get GPS Data (PDF #166)
```bash
curl -X POST http://localhost:8000/api/v1/commands/GetGpsData \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"GetGpsData","payload":{}}'
```

---

### 18. PRICE BOARDS

#### Get Price Board Status (PDF #168)
```bash
curl -X POST http://localhost:8000/api/v1/commands/PriceBoardGetStatus \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PriceBoardGetStatus","payload":{"PriceBoard":1}}'
```

---

### 19. READERS

#### Get Reader Tag (PDF #170)
```bash
curl -X POST http://localhost:8000/api/v1/commands/ReaderGetTag \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"ReaderGetTag","payload":{"Reader":1}}'
```

#### Get Reader Status (PDF #172)
```bash
curl -X POST http://localhost:8000/api/v1/commands/ReaderGetStatus \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"ReaderGetStatus","payload":{"Reader":1}}'
```

---

### 20. PAYMENTS

#### Create Payment Transaction (PDF #174)
```bash
curl -X POST http://localhost:8000/api/v1/commands/PaymentCreateTransaction \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PaymentCreateTransaction","payload":{"Pump":1,"Nozzle":1,"Type":"Amount","Dose":50.00,"Price":2.80}}'
```

#### Get Payment Transaction Info (PDF #176)
```bash
curl -X POST http://localhost:8000/api/v1/commands/PaymentGetTransactionInformation \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PaymentGetTransactionInformation","payload":{"Pump":1,"Transaction":1}}'
```

#### Refund Payment Transaction (PDF #178)
```bash
curl -X POST http://localhost:8000/api/v1/commands/PaymentRefundTransaction \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"PaymentRefundTransaction","payload":{"Pump":1,"Transaction":1}}'
```

---

### 21. SHIFT MANAGEMENT

#### Open Shift (PDF #179)
```bash
curl -X POST http://localhost:8000/api/v1/commands/ShiftOpen \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"ShiftOpen","payload":{}}'
```

#### Close Shift (PDF #181)
```bash
curl -X POST http://localhost:8000/api/v1/commands/ShiftClose \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"ShiftClose","payload":{}}'
```

#### Get Shift Information (PDF #182)
```bash
curl -X POST http://localhost:8000/api/v1/commands/ShiftGetInformation \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"ShiftGetInformation","payload":{}}'
```

---

### 22. REPORTS

All report requests require `DateTimeStart` and `DateTimeEnd`.

#### Pump Transactions Report (PDF #184)
```bash
curl -X POST http://localhost:8000/api/v1/commands/ReportGetPumpTransactions \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"ReportGetPumpTransactions","payload":{"Pump":0,"DateTimeStart":"2026-03-01T00:00:00","DateTimeEnd":"2026-03-31T23:59:59"}}'
```

#### Tank Measurements Report (PDF #186)
```bash
curl -X POST http://localhost:8000/api/v1/commands/ReportGetTankMeasurements \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"ReportGetTankMeasurements","payload":{"Probe":1,"DateTimeStart":"2026-03-01T00:00:00","DateTimeEnd":"2026-03-31T23:59:59"}}'
```

#### In-Tank Deliveries Report (PDF #188)
```bash
curl -X POST http://localhost:8000/api/v1/commands/ReportGetInTankDeliveries \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"ReportGetInTankDeliveries","payload":{"Probe":1,"DateTimeStart":"2026-03-01T00:00:00","DateTimeEnd":"2026-03-31T23:59:59"}}'
```

#### GPS Records Report (PDF #190)
```bash
curl -X POST http://localhost:8000/api/v1/commands/ReportGetGpsRecords \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"ReportGetGpsRecords","payload":{"DateTimeStart":"2026-03-01T00:00:00","DateTimeEnd":"2026-03-31T23:59:59"}}'
```

#### Alert Records Report (PDF #192)
```bash
curl -X POST http://localhost:8000/api/v1/commands/ReportGetAlertRecords \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"ReportGetAlertRecords","payload":{"DateTimeStart":"2026-03-01T00:00:00","DateTimeEnd":"2026-03-31T23:59:59"}}'
```

#### Payments Report (PDF #194)
```bash
curl -X POST http://localhost:8000/api/v1/commands/ReportGetPayments \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"ReportGetPayments","payload":{"DateTimeStart":"2026-03-01T00:00:00","DateTimeEnd":"2026-03-31T23:59:59"}}'
```

#### Shifts Report (PDF #196)
```bash
curl -X POST http://localhost:8000/api/v1/commands/ReportGetShifts \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"ReportGetShifts","payload":{"DateTimeStart":"2026-03-01T00:00:00","DateTimeEnd":"2026-03-31T23:59:59"}}'
```

---

### 23. DIAGNOSTICS

#### Run Diagnostics (PDF #198)
```bash
curl -X POST http://localhost:8000/api/v1/commands/MakeDiagnostics \
  -H "X-API-Key: change_me_api_key" \
  -H "Content-Type: application/json" \
  -d '{"action":"MakeDiagnostics","payload":{}}'
```

---

## Your Device Reference

Based on your PTS device response:

| Fuel Grade ID | Name | Current Price |
|---|---|---|
| 1 | Petrol | 2.80 |
| 2 | Diesel | 4.50 |
| 3 | (LPG/Other) | 3.75 |

| Pump | Active Nozzles | Nozzle Prices |
|---|---|---|
| Pump 1 | 3 | [2.80, 4.50, 3.75, 0, 0, 0] |
| Pump 2 | 3 | [2.80, 4.50, 3.75, 0, 0, 0] |
| Pump 3 | 3 | [3.75, 2.80, 4.50, 0, 0, 0] |
| Pump 4 | 3 | [3.75, 2.80, 4.50, 0, 0, 0] |

---

## Health & Status Endpoints

These don't need the commands endpoint:

```bash
# Health check
curl http://localhost:8000/health

# Backend status
curl -H "X-API-Key: change_me_api_key" http://localhost:8000/api/v1/status/backend

# Device connection status
curl -H "X-API-Key: change_me_api_key" http://localhost:8000/api/v1/status/device
```

---

## Notes

- **Python 3.11.x** required; **3.11.9** is the validated project version (see root `README.md` and `.python-version`)
- **PTS_AUTH_MODE=digest** in `.env`
- **PTS_VERIFY_SSL=false** for self-signed certificate
- All commands are audited in the database
- Interactive API docs: `http://localhost:8000/docs`
- The `PDF #` references the section number in the jsonPTS protocol PDF
- Replace `localhost` with your server IP when calling from another machine
