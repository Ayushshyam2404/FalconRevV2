# Falcon Rev — Integration Guide

This guide explains how an external application (your friend's software) can share **one Excel upload** with Falcon Rev. Both systems process the same file without duplicating uploads or storage.

---

## Overview

```
Your Friend's App
       │
       │  1. POST /api/upload  (multipart, the Excel file)
       ▼
  Falcon Rev Server
       │
       │  Returns: JSON with daily_data, metrics, competitor_pricing
       │
       ├──► Your Friend's App uses the JSON for its own logic
       │
       └──► POST /api/send-email  (optional — trigger Falcon Rev email)
```

---

## Base URL

Replace `<FALCON_REV_HOST>` with wherever Falcon Rev is running:
- Local dev: `http://localhost:3000`
- Production: your deployed URL

---

## Endpoints

### 1. `POST /api/upload` — Upload & process the Excel file

```
POST <FALCON_REV_HOST>/api/upload
Content-Type: multipart/form-data
Body:  file=<StrategicAnalysis.xlsx>
```

**cURL example:**
```bash
curl -X POST http://localhost:3000/api/upload \
  -F "file=@/path/to/StrategicAnalysis.xlsx"
```

**Python example:**
```python
import requests

with open("StrategicAnalysis.xlsx", "rb") as f:
    resp = requests.post(
        "http://localhost:3000/api/upload",
        files={"file": f}
    )

result = resp.json()
data   = result["data"]  # use this in your own app

daily_data         = data["daily_data"]         # list of daily rows
metrics            = data["metrics"]            # summary KPIs
competitor_pricing = data["competitor_pricing"] # per-day competitor rates
```

**Response shape:**
```json
{
  "success": true,
  "filename": "StrategicAnalysis.xlsx",
  "data": {
    "daily_data": [
      {
        "date": "Mon 5/26",
        "adr": 149.0,
        "revenue": 12540.0,
        "rooms_sold": 84,
        "pickup": 3
      }
    ],
    "metrics": {
      "avg_adr":     149.0,
      "total_revenue": 87780.0,
      "avg_occupancy": 84.0
    },
    "competitor_pricing": [
      {
        "date": "Mon 5/26",
        "competitors": [
          { "name": "Hampton Inn",    "rate": 152.0 },
          { "name": "Hilton Garden",  "rate": 161.0 },
          { "name": "Holiday Inn",    "rate": 139.0 },
          { "name": "Hyatt Place",    "rate": 155.0 }
        ]
      }
    ]
  }
}
```

---

### 2. `GET /api/latest-data` — Retrieve the last processed data

If your software wants to poll for the most recently uploaded file (e.g., after a user uploads through the Falcon Rev web portal):

```bash
curl http://localhost:3000/api/latest-data
```

Returns the same `data` shape as `/api/upload`. Returns `404` if nothing has been uploaded yet.

---

### 3. `POST /api/send-email` — Trigger the Falcon Rev email report

After processing, you can tell Falcon Rev to send the report email:

```bash
curl -X POST http://localhost:3000/api/send-email \
  -H "Content-Type: application/json" \
  -d '{
    "email":        "manager@hotel.com",
    "subject":      "Revenue Report - May 26",
    "report_theme": "dark",
    "data":         <paste the data object from /api/upload response>
  }'
```

**Python example (end-to-end):**
```python
import requests

# Step 1: upload Excel (one upload, shared)
with open("StrategicAnalysis.xlsx", "rb") as f:
    upload_resp = requests.post(
        "http://localhost:3000/api/upload",
        files={"file": f}
    ).json()

data = upload_resp["data"]

# Step 2: use data in your own app
process_in_your_app(data)

# Step 3: also send Falcon Rev email report
requests.post(
    "http://localhost:3000/api/send-email",
    json={
        "email":        "manager@hotel.com",
        "subject":      "Falcon Rev Report",
        "report_theme": "dark",   # or "light"
        "data":         data
    }
)
```

---

## Shared Filesystem Alternative

If both apps run on the **same server**, you can avoid HTTP entirely:

1. Your software saves the Excel file to a shared path (e.g., `/shared/reports/latest.xlsx`).
2. Falcon Rev provides a `POST /api/upload` call pointing at that path **or** you import the processor directly:

```python
# Inside your_app.py (same server as Falcon Rev)
import sys
sys.path.insert(0, "/path/to/FLrevV2")

from utils.excel_processor import process_excel_file

data = process_excel_file("/shared/reports/latest.xlsx")
# data is now available to both apps without any HTTP round-trip
```

---

## Excel File Format Requirements

Falcon Rev expects the **original StrategicAnalysis Excel format** with columns at specific positions.
Changing column order or headers will break extraction silently. Key columns:

| Data              | Column(s)             |
|-------------------|-----------------------|
| Date label        | A or first column     |
| ADR               | Auto-detected         |
| Revenue           | Auto-detected         |
| Rooms Sold        | Auto-detected         |
| Pickup            | Auto-detected         |
| Competitor rates  | `Unnamed: 68` – `Unnamed: 75` |

Do **not** modify the Excel template column layout.

---

## CORS / Security Notes

- Falcon Rev currently has no API key. If exposed publicly, add `Flask-CORS` and a secret header check.
- All data is processed in memory; nothing is persisted beyond the upload session except the uploaded file itself (in `uploads/`).
- The `GET /api/latest-data` endpoint returns whatever was last uploaded — it is **not** user-isolated. This is fine for a single-hotel deployment.
