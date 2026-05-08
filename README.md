# 📖 AirLib

AirLib is a personal tool to convert physical book pages into EPUBs you can read on your phone. It's built for a very specific use case: you want to read a book during short moments of the day without carrying it around.

The flow is simple — take photos of the pages you want to read, send them to the server, and get back an EPUB ready to open in Apple Books or any other reader.

---

## What is this for, exactly?

This is not a book digitizer. It's not meant to scan entire books or archive anything.

It's for this: you have 15 minutes on the train, you want to read the next few pages of your book but you don't have it with you. Before leaving home, you take photos of today's pages, send them to AirLib, and save the EPUB on your phone.

Each session generates an independent fragment. There's no database, no history, nothing stored on the server.

---

## How it works

1. Send one or more photos of book pages to the `/epub` endpoint
2. Each image is sent to GPT-4o Vision, which transcribes the text and formats it in HTML
3. The server generates an EPUB with all the content and returns it directly
4. Open the EPUB in Apple Books or any EPUB reader

---

## Requirements

- Python 3.10+
- An OpenAI API key with access to GPT-4o
- The server accessible from your phone (via local network, VPN, reverse proxy, or any method you prefer)

---

## Installation

```bash
git clone https://github.com/yourusername/airlib
cd airlib
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the root of the project:

```
OPENAI_API_KEY=sk-...
```

Start the server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## Usage

### From the terminal

```bash
curl -X POST http://<your-server-ip>:8000/epub \
  -F "file=@page.jpg" \
  -F "book_title=My Book" \
  -o fragment.epub
```

### From iPhone (Apple Shortcuts)

AirLib works well with the Apple Shortcuts app, which can send photos directly to the server and open the resulting EPUB in Apple Books.

A basic Shortcut looks like this:

1. **Ask for input** — prompt for the book title
2. **Select photos** — pick the pages you want to read (select multiple)
3. **Convert image** — convert each photo to JPEG (iPhones shoot in HEIC by default, which is not supported by OpenAI)
4. **Get contents of URL** — POST to `http://<your-server-ip>:8000/epub` with:
   - Method: POST
   - Body: Multipart Form
   - Field `book_title`: the title from step 1
   - Field `file`: the converted photo(s)
5. **Set name** — rename the result to `<title>.epub`
6. **Save file** — save to Files or iCloud
7. **Open file** — open in Apple Books

> **Note:** iPhones shoot in HEIC format. Make sure to convert photos to JPEG before sending, otherwise OpenAI will reject them.

> **Multi-image support via Shortcuts is a work in progress.** Currently, Shortcuts has limitations when sending multiple files in a single multipart request. Single-image scanning works reliably end-to-end.

### From Android

HTTP Shortcuts is a good alternative to Apple Shortcuts on Android.

---

## Stack

| Component | Technology |
|---|---|
| Backend | Python + FastAPI |
| OCR & formatting | OpenAI GPT-4o Vision |
| EPUB generation | ebooklib |
| Client | Apple Shortcuts → Apple Books |

---

## Limitations

- Requires a running server — does not work offline
- Transcription quality depends on photo quality (good lighting, flat page)
- Uses the OpenAI API, which has a cost (minimal for this use — cents per session)
- Multi-image support via Shortcuts is currently limited by how the app handles multipart form requests
- This is a personal tool for occasional, private use

---

## Project structure

```
airlib/
├── main.py
├── requirements.txt
├── .env          # do not commit
└── README.md
```
