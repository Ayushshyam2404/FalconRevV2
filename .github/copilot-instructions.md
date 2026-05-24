# Copilot Instructions — Falcon Rev

## Project Overview

Flask web application that processes hotel revenue Excel files and sends formatted HTML email reports. Single-page dark/orange themed UI with three API endpoints.

## Running the App

```bash
# Install dependencies
pip install -r requirements.txt

# Start server (runs on port 3000)
python3 app.py

# Test SMTP connection only
python3 test_email.py
```

## Architecture

```
app.py                       # Flask entry point — 4 routes + SMTP send logic
utils/excel_processor.py     # All Excel parsing logic
utils/email_generator.py     # HTML email template + HTML-to-image via Selenium
templates/index.html         # Single-page UI (all CSS/JS inline)
static/                      # favicon and other static assets
uploads/logos/               # Runtime logo storage (gitignored)
```

### Request flow for sending a report

1. `POST /api/upload` → `process_excel_file()` → returns parsed JSON
2. `POST /api/upload-logo` → reads file, returns base64 data URI directly (no disk write)
3. `POST /api/send-email` → `generate_email_html()` → `convert_html_to_image()` (Selenium headless Chrome) → SMTP inline-image send

The email is sent as a **screenshot of the HTML** (a PNG attached inline via CID), not as raw HTML. `selenium` is required for `convert_html_to_image()` to work.

## Excel File Format

The processor hard-codes column positions — do not change them without updating `excel_processor.py`:

| Data | Column name |
|------|-------------|
| Date | `Unnamed: 1` |
| Pickups | `Transient` |
| ADR | `ADR` |
| Occupancy | `On the Books` |
| Competitor rates | `Unnamed: 68` – `Unnamed: 75` |

Row 0 is the header; row 1 is skipped (it contains label text); data rows start at index 1 after `df.iloc[1:].reset_index()`. Only the first 7 rows are processed (7-day forecast).

The eight competitor hotels are mapped positionally to columns 68–75:
`Candlewood Suites`, `Comfort Suites`, `Fairfield Inn`, `Hampton Int`, `Hilton Garden`, `Holiday Inn`, `Hyatt Place`, `Residence Inn`.

Revenue is **calculated** (not a raw column): `occupancy% / 100 × ADR × 100 rooms`.

## Environment Variables

Create a `.env` file (see `.env.example`). The active code in `app.py` reads:

```
SMTP_HOST=smtp.ionos.com
SMTP_PORT=587
SMTP_USERNAME=your@email.com
SMTP_PASSWORD=your_password
SENDER_EMAIL=your@email.com   # optional, defaults to SMTP_USERNAME
```

> **Note:** `.env.example` still references the old `SENDER_EMAIL`/`SENDER_PASSWORD`/`SMTP_SERVER` names from an earlier Gmail integration — those are only used by `test_email.py`, not by the live `send_smtp_email()` function in `app.py`.

## Key Conventions

- All API responses use `{'success': True, ...}` on success and `{'error': '...'}` with a 4xx/5xx status on failure.
- Logo images are **never saved to disk** — they are converted to base64 data URIs in memory and passed through the JSON payload to `generate_email_html()`.
- All inline styles in the email template use double braces `{{ }}` because the HTML is built inside a Python f-string.
- `app.run(debug=True, port=3000)` is the default; README mentions port 9000 — use the value in `app.py` as the source of truth.
- The `uploads/` folder is created at startup with `os.makedirs(..., exist_ok=True)` — never assume it pre-exists.
