# Image to Text

import os
import base64
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage


load_dotenv()


def main():
    print("Hello from Designer Agent!")

    llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash', temperature=0)

    message_url = HumanMessage(
        content=[
            {
                "type": "text",
                "text": "Describe the image at the URL.",
            },
            {
                "type": "image_url",
                "image_url": "https://picsum.photos/seed/picsum/200/300",
            }
        ]
    )

    # result_url = llm.invoke([message_url])
    # print(f"Response for URL image: {result_url.content}")

    image_file_path = "/Users/maakhan/Desktop/langchain-course/image_local.png"

    with open(image_file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    message_local = HumanMessage(
    content=[
            {
                "type": "text", 
                "text": "Describe the local image.",
            },
            {
                "type": "image_url", 
                "image_url": f"data:image/png;base64,{encoded_image}",
            },
        ]
    )

    result_local = llm.invoke([message_local])
    print(f"Response for local image: {result_local.content}")
    # messages = [
    #     (
    #         "system",
    #         "You are a helpful assistant.",
    #     ),
    #     ("human", "In one para tell me what is LangChain"),
    # ]

    # ai_msg = llm.invoke(messages)
    # print(ai_msg.content)

    # response = llm.invoke(
    #     "Generate an image of a cat wearing a hat",
    #     generation_config=dict(response_modalities=["TEXT", "IMAGE"]),
    # )

    # image_base64 = response.content[0].get("image_url").get("url").split(",")[-1]
    # image_data = base64.b64decode(image_base64)

if __name__ == "__main__":
    main()
