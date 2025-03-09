from diffusers import StableDiffusionImg2ImgPipeline, DPMSolverMultistepScheduler,AutoPipelineForText2Image

import torch
from PIL import Image

def create_image(img_path,device):
    # 利用したいAIモデル
    model_id = "CompVis/stable-diffusion-v1-4"

    # パイプラインの作成
    pipeline  = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, torch_dtype=torch.float16, safety_checker=None)
    pipeline.scheduler = DPMSolverMultistepScheduler.from_config(pipeline.scheduler.config)

    # GPUを使うように変更
    try:
        pipeline = pipeline.to(device)
    except:
        print("No GPU found, using CPU")
    init_image = Image.open(img_path)
    width, height = 800, 600  # 4:3のアスペクト比にリサイズ
    init_image = init_image.resize((width, height))
    prompt="childlike drawing, rough sketch, simple shapes, uneven lines, imperfect proportions, crayon style, doodle, playful, colorful, elementary school art, basic figures, simple backgrounds, spontaneous, naive art"
    image = pipeline (prompt=prompt, image=init_image, strength=0.6, num_inference_steps=30).images[0]

    # 生成画像を表示
    image.save("./photo/result.png")
def create_image_sdx(prompt,device):
    pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16")
    pipe.to(device)
    prompt = prompt

    image = pipe(prompt=prompt, num_inference_steps=1, guidance_scale=0.0).images[0]
    image.save("./photo/result.png")

    return image
