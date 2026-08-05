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

1. Take photos of the pages you want to read and convert them to JPEG
2. Send each photo, one at a time, to the `/transcribe` endpoint — it returns the transcribed HTML for that page
3. Collect the transcribed pages, in order, on the client
4. Send the book title and the full list of transcribed pages to the `/epub` endpoint
5. The server builds an EPUB with all the content and returns it directly
6. Open the EPUB in Apple Books or any EPUB reader

Photos are sent one per request instead of all at once because Apple Shortcuts cannot reliably attach a list of files to a single form field in one `POST` — see [Limitations](#limitations).

---

## Requirements

- Python 3.10+
- An OpenAI API key with access to GPT-4o
- The server accessible from your phone (via local network, VPN, reverse proxy, or any method you prefer)

---

## Installation

```bash
git clone https://github.com/camilokurk/AirLib
cd AirLib
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
uvicorn main:app --host 0.0.0.0 --port 2010
```

---

## Usage

### From the terminal

```bash
# One request per page
curl -X POST http://<your-server-ip>:2010/transcribe \
  -F "file=@page1.jpg"
  # => {"contenido": "<p>...</p>"}

# Then build the EPUB from the collected pages
curl -X POST http://<your-server-ip>:2010/epub \
  --form-string "contenido=<p>Page 1 text...</p>" \
  --form-string "contenido=<p>Page 2 text...</p>" \
  -F "book_title=My Book" \
  -o fragment.epub
```

### From iPhone (Apple Shortcuts)

AirLib works well with the Apple Shortcuts app, which can send photos directly to the server and open the resulting EPUB in Apple Books.

A basic Shortcut looks like this:

1. **Ask for input** — prompt for the book title
2. **Select photos** — pick the pages you want to read (select multiple)
3. **Repeat with each** photo:
   - **Convert image** to JPEG (iPhones shoot in HEIC by default, which is not supported by OpenAI)
   - **Get contents of URL** — POST to `http://<your-server-ip>:2010/transcribe` with the converted photo as a File field named `file`
   - **Get dictionary value** — pull `contenido` out of the JSON response
   - **Add to variable** — append it to a list variable (e.g. `Pages`)
4. **Get contents of URL** — POST to `http://<your-server-ip>:2010/epub` with:
   - Method: POST
   - Body: Form
   - Field `book_title` (type Text): the title from step 1
   - Field `contenido` (type Text): the `Pages` list — Shortcuts sends one form field per list item
5. **Set name** — rename the result to `<title>.epub`
6. **Save file** — save to Files or iCloud
7. **Open file** — open in Apple Books

> **Note:** iPhones shoot in HEIC format. Make sure to convert photos to JPEG before sending, otherwise OpenAI will reject them.

> **Why one photo per request instead of all at once?** Apple Shortcuts cannot attach a list of files to a single `File` field in a `POST` request — only one image ends up being sent, no matter how many were selected, and the "Make Archive" workaround proved unreliable in practice (it intermittently zipped iOS's unresolved-file placeholder icon instead of the real photo). Sending one photo per request and accumulating the transcribed text in a Shortcuts list variable sidesteps both problems.

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
- Transcribing happens one photo per request; the client is responsible for collecting the pages in order before calling `/epub`
- This is a personal tool for occasional, private use

---

## Project structure

```
airlib/
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example  # copy to .env and fill in your key
├── .env          # do not commit
└── README.md
```
