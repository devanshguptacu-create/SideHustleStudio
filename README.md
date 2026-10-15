# SideHustle Studio

**A local-first AI listing writer for small sellers and side hustlers.**

SideHustle Studio turns seller-provided product facts into an editable title, description, benefits, call to action, and tags for Instagram, Etsy, eBay, WhatsApp Business, Facebook Marketplace, and Shopify.

## Why this project?

Independent sellers often spend too much time writing product listings. This tool helps them create a useful first draft without requiring a paid hosted AI API. It uses an open-weight language model served locally by Ollama.

## Features

- Listing generation from seller-provided facts
- Platform, tone, audience, price, and language choices (English, Hindi, Hinglish)
- Copy and download the generated draft
- Responsive layout
- Local model inference through Ollama
- Prompt guardrails against inventing product claims

## Tech stack

- HTML5, CSS3, vanilla JavaScript
- Python + Flask backend (required)
- Ollama local inference
- Default model: `qwen2.5:3b`

## Project structure

```text
SideHustleStudio/
├── app.py
├── requirements.txt
├── index.html
├── style.css
├── script.js
└── README.md
```

## Run locally on Windows

**Important:** Opening `index.html` directly will not run the AI. The frontend calls `/api/generate`, so you must run the Flask backend and Ollama.

1. Install Python from https://www.python.org/downloads/
2. Install Ollama from https://ollama.com/
3. In a terminal, download the model:

   ```powershell
   ollama pull qwen2.5:3b
   ```

4. Install the Python dependencies:

   ```powershell
   py -m pip install Flask requests
   ```

5. Put the companion `app.py` in the same folder as `index.html`. The Flask app must serve `index.html`, `style.css`, and `script.js` from the same project, and implement `POST /api/generate` by sending the prompt to Ollama's local API. If you downloaded the full SideHustle Studio starter ZIP, use its `app.py` and `requirements.txt`.
6. Run the Flask app:

   ```powershell
   py app.py
   ```

7. Open the local URL printed by Flask (usually http://127.0.0.1:5000).

## Open innovation and privacy

The app is designed around local inference. Product details are sent to the Ollama service running on your computer, not a hosted AI API by this app. The model can be switched and the prompt can be inspected or customized. Local privacy still depends on your computer and installed software; avoid entering sensitive customer information.

## Model licensing and commercial use

The default model is `qwen2.5:3b`. Review its current model card, license, and applicable usage terms before commercial use. Generated copy can be wrong, so sellers should verify prices, specifications, and claims before publishing.

## Limitations and roadmap

- Prototype, not a production multi-user service
- No product-image analysis or direct publishing yet
- Model speed depends on computer hardware
- Planned: saved brand voices, product-photo assistance, export presets, more languages, and feedback from real sellers

## Contributing

Issues and pull requests are welcome. Do not commit API keys, private customer information, or downloaded model files.

## License

Add a `LICENSE` file before presenting the repository as open-source for reuse. Choose a license only after reviewing its terms.
