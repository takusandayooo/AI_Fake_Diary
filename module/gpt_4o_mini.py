from openai import OpenAI
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

def create_image_prompt(prompt):
    client = OpenAI()

    system_prompt = """
        あなたのタスクは、日記の文章をもとに、ユーモアのあるイラストや漫画風の画像を生成するプロンプトを作成することです。

        ### **手順**
        1. **日記の内容を分析**:
        - 重要な出来事、登場人物、感情を抽出する。
        - 面白い要素を強調する。

        2. **視覚的な要素を明確にする**:
        - どんなシーンか？（例：オフィスで寝落ちする、猫と会話する など）
        - どんなキャラクターがいるか？（例：人間、動物、モンスター など）
        - どんな表情・動きか？（例：驚き、喜び、困惑 など）

        3. **画像のスタイルを決定する**:
        - コミカルな漫画風 / デフォルメイラスト / シンプルなスケッチ など
        - 背景の有無（簡単な背景 or 詳細な背景）

        4. **プロンプトを出力する**:
        - 具体的な指示（キャラクター、シチュエーション、アートスタイルなど）
        - 適切な英語で表現する（AIが画像生成しやすいように）

        ### **出力例**
        【入力】  
        日記：「今日は仕事中にコーヒーをこぼしてしまった。服がコーヒーまみれになって悲しかったけど、同僚が『新しいファッションだね』と笑わせてくれた。」

        【出力（画像生成プロンプト）】  
        "A cartoon-style illustration of an office worker with a shocked expression, spilling coffee all over their shirt. Their colleague is laughing and pointing, saying 'New fashion trend!'. The scene is set in a modern office, with desks and computers in the background. The style is humorous and lighthearted."
        このように、日記の内容を分析し、視覚的に面白い画像を生成するためのプロンプトを作成してください。
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content
