# Image Generation

> Gemini multimodal pipeline: text-to-image generation and image-to-image style transfer using Google's Gemini 2.0 Flash image generation model.

## Architecture

```
Text Prompt [+ optional input image]
    │
    ▼
ChatGoogleGenerativeAI
(gemini-2.0-flash-preview-image-generation)
response_modalities=["TEXT", "IMAGE"]
    │
    ├── text content  ──► print description
    └── image_url     ──► base64 decode ──► PIL.Image ──► save .png
```

## Key Concepts
- Gemini's `response_modalities=["TEXT", "IMAGE"]` to request multimodal output
- Extracting base64 image data from the `image_url` block in the response
- Image-to-image transfer: encoding input as base64 and passing in message content
- `learning/` subdirectory contains step-by-step progression scripts

## Tech Stack
- `langchain-google-genai` · Google Gemini 2.0 Flash · PIL (Pillow) · `python-dotenv`

## How to Run
1. Copy `.env.example` to `.env` and fill in `GOOGLE_API_KEY`
2. `cd multimodal/image-generation`
3. Install deps: `pip install langchain-google-genai pillow python-dotenv`
4. Run: `python image-gen.py`
5. Output saved as `van-gogh-v2.png` in current directory

## What I Learned
Gemini's image generation API is notably different from OpenAI's DALL-E: it returns image data inline in the chat message (as a base64 `image_url` block) rather than as a separate URL endpoint. The `response_modalities` parameter must be set in `generation_config`, not in the standard LangChain invoke kwargs — this is a Gemini-specific pattern that the LangChain wrapper exposes via a passthrough.
