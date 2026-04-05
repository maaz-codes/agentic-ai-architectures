# Text to Image

import base64
import io

from PIL import Image
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv


load_dotenv()


llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash-image-preview")

message = {
    "role": "user",
    "content": "Generate a photorealistic image of a cuddly cat wearing a hat.",
}

response = llm.invoke(
    [message],
    generation_config=dict(response_modalities=["TEXT", "IMAGE"]),
)


def _get_image_base64(response: AIMessage) -> None:
    image_block = next(
        block
        for block in response.content
        if isinstance(block, dict) and block.get("image_url")
    )
    return image_block["image_url"].get("url").split(",")[-1]


image_base64 = _get_image_base64(response)

# save the image
image_bytes = base64.b64decode(image_base64)
image = Image.open(io.BytesIO(image_bytes))
image.save('cat_with_hat.png')
