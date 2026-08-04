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
2. Bundle the photos into a single `.zip` file (in order) and send it to the `/epub` endpoint
3. The server extracts each image and sends it to GPT-4o Vision, which transcribes the text and formats it in HTML
4. The server generates an EPUB with all the content, in the same order as the zip, and returns it directly
5. Open the EPUB in Apple Books or any EPUB reader

A single zipped file is used instead of multiple files in one multipart request because Apple Shortcuts cannot reliably attach more than one file to the same form field in a single `POST` — see [Limitations](#limitations).

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
  -F "file=@pages.zip" \
  -F "book_title=My Book" \
  -o fragment.epub
```

`pages.zip` should contain one or more `.jpg`/`.jpeg`/`.png` images, ordered the way you want them to appear in the EPUB.

### From iPhone (Apple Shortcuts)

AirLib works well with the Apple Shortcuts app, which can send photos directly to the server and open the resulting EPUB in Apple Books.

A basic Shortcut looks like this:

1. **Ask for input** — prompt for the book title
2. **Select photos** — pick the pages you want to read (select multiple)
3. **Repeat with each** photo → **Convert image** to JPEG (iPhones shoot in HEIC by default, which is not supported by OpenAI)
4. **Make Archive** — zip the results of the repeat step into a single `.zip` file
5. **Get contents of URL** — POST to `http://<your-server-ip>:8000/epub` with:
   - Method: POST
   - Body: Form
   - Field `book_title` (type Text): the title from step 1
   - Field `file` (type File): the `.zip` from step 4
6. **Set name** — rename the result to `<title>.epub`
7. **Save file** — save to Files or iCloud
8. **Open file** — open in Apple Books

> **Note:** iPhones shoot in HEIC format. Make sure to convert photos to JPEG before zipping, otherwise OpenAI will reject them.

> **Why a zip and not multiple form fields?** Apple Shortcuts cannot attach a list of files to a single `File` field in a `POST` request — only one image ends up being sent, no matter how many were selected. Zipping the photos client-side and sending one file sidesteps that limitation entirely.

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
- The `/epub` endpoint expects a single `.zip` of images, not raw multipart files, due to the Apple Shortcuts limitation described above
- This is a personal tool for occasional, private use

---

## Project structure

```
airlib/
├── main.py
├── requirements.txt
├── .env.example  # copy to .env and fill in your key
├── .env          # do not commit
└── README.md
```
