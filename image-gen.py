import base64
import io

from PIL import Image
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv


load_dotenv()


nano_banana = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash-image-preview")
llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash-preview-image-generation")


def _get_image_base64(response: AIMessage) -> None:
    image_block = next(
        block
        for block in response.content
        if isinstance(block, dict) and block.get("image_url")
    )
    return image_block["image_url"].get("url").split(",")[-1]


def save_image_to_local(response: AIMessage):
    print("Saving Image...")

    image_base64 = _get_image_base64(response)

    image_bytes = base64.b64decode(image_base64)
    image = Image.open(io.BytesIO(image_bytes))
    image.save('van-gogh-v2.png')


def generate_image(prompt: str, image: str = None, model: ChatGoogleGenerativeAI = llm) -> str:
    print("Generating Image...")

    content = [{
        "type": "text",
        "text": prompt,
    }]

    if image:
        with open(image, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        content.append({
            "type": "image_url",
            "image_url": f"data:image/png;base64,{encoded_image}",
        })

    message = {
        "role": "user",
        "content": content,
    }

    result = model.invoke(
        input=[message],
        generation_config=dict(response_modalities=["TEXT", "IMAGE"]),
    )

    save_image_to_local(result)

    text_response = result.content[0]
    return text_response


def main():
    print("Hello from Nano-Banana!")

    image_path = "/Users/maakhan/Desktop/langchain-course/image_local.png"
    response = generate_image(
        prompt="Create this image into a Vincent van Gogh painting",
        image=image_path,
        model=nano_banana,
    )
    print(response)


if __name__ == "__main__":
    main()
