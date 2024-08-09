from openai import OpenAI
import os
import base64


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def make_nikki_from_image(image_path, OPENAI_API_KEY):
    client = OpenAI(api_key=OPENAI_API_KEY)
    base64_image = encode_image(image_path) 

    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "あなたは絵日記を書く子どもです。見た画像を元に、まるで日記を書いているかのように文章を作成してください。子どもらしい簡単で親しみやすい言葉を使ってください。"},
            {"role": "user", "content": [
                {"type": "text", "text": "この画像を見て、絵日記のように160文字以内で説明してみてください。"},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
            ]}
        ],
        temperature=0.0,
    )
    result=response.choices[0].message.content
    return result
