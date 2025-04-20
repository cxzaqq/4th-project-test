# image_server.py
from fastapi import FastAPI, Request
from diffusers import StableDiffusionPipeline
import torch
import os

app = FastAPI()

# 이미지 저장 폴더 생성
os.makedirs("generated", exist_ok=True)

# 모델 로드 (CPU용)
pipe = StableDiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-2-1"
)
pipe = pipe.to("cpu")  # GPU 대신 CPU

@app.post("/generate")
async def generate_image(request: Request):
    body = await request.json()
    prompt = body.get("prompt", "a cozy empty garden in watercolor style")
    image = pipe(prompt).images[0]
    
    # 파일명 단순화
    filename = f"{prompt[:30].replace(' ', '_')}.png"
    filepath = f"generated/{filename}"
    
    image.save(filepath)
    return {"image_url": filepath}