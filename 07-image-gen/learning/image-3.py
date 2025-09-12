# Image + Text to Image

import base64
import io

from PIL import Image
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv


load_dotenv()


image_file_path = "/Users/maakhan/Desktop/langchain-course/image_local.png"
with open(image_file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")


# llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash-image-preview")
llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash-preview-image-generation")

message = {
    "role": "user",
    "content": [
        {
            "type": "text",
            "text": "Convert this image into a Vincent van Gogh Painting",
        },
        {
            "type": "image_url",
            "image_url": f"data:image/png;base64,{encoded_image}",
        }
    ],
}

response = llm.invoke(
    [message],
    generation_config=dict(response_modalities=["TEXT", "IMAGE"]),
)

text_response = response.content[0]
image_response = response.content[1]

print(text_response)

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
image.save('maakhan-van-gogh-v1.png')
