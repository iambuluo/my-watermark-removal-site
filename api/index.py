import os

# Set cache directories to /tmp for Vercel Serverless environment
os.environ["TORCH_HOME"] = "/tmp/torch"
os.environ["XDG_CACHE_HOME"] = "/tmp/cache"

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import torch
import cv2
import numpy as np
from PIL import Image
import io

# Relative imports for Vercel
from .model import LaMa
from .schema import InpaintRequest
from .utils import load_img, pil_to_bytes, concat_alpha_channel

app = FastAPI()

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None

def get_model():
    global model
    if model is None:
        print("Loading model...")
        device = torch.device("cpu")
        model = LaMa(device)
        print("Model loaded.")
    return model

@app.get("/api/hello")
def hello():
    return {"message": "Hello from IOPaint Vercel"}

@app.post("/api/inpaint")
async def inpaint(
    image: UploadFile = File(...),
    mask: UploadFile = File(...),
    hd_strategy: str = Form("Original"),
    ldm_steps: int = Form(50),
    ldm_sampler: str = Form("plms"),
    zits_wireframe: bool = Form(True),
    prompt: str = Form(""),
    negative_prompt: str = Form(""),
):
    try:
        # Read image and mask
        image_bytes = await image.read()
        mask_bytes = await mask.read()

        rgb_np_img, alpha_channel, infos = load_img(image_bytes, return_info=True)
        mask_np_img, _, _ = load_img(mask_bytes, gray=True, return_info=True)

        # Binarize mask
        mask_np_img = cv2.threshold(mask_np_img, 127, 255, cv2.THRESH_BINARY)[1]

        if rgb_np_img.shape[:2] != mask_np_img.shape[:2]:
             raise HTTPException(
                status_code=400,
                detail=f"Image size({rgb_np_img.shape[:2]}) and mask size({mask_np_img.shape[:2]}) not match.",
            )

        # Create request object
        req = InpaintRequest(
            image="", # Not used in internal logic if we pass processed arrays
            mask="",  # Not used
            hd_strategy=hd_strategy,
            ldm_steps=ldm_steps,
            ldm_sampler=ldm_sampler,
            zits_wireframe=zits_wireframe,
            prompt=prompt,
            negative_prompt=negative_prompt,
        )

        # Run model
        lama_model = get_model()
        bgr_res = lama_model(rgb_np_img, mask_np_img, req)

        # Post-process
        rgb_res = cv2.cvtColor(bgr_res.astype(np.uint8), cv2.COLOR_BGR2RGB)
        rgb_res = concat_alpha_channel(rgb_res, alpha_channel)

        # Convert to bytes
        ext = "png" # Default to png
        res_img_bytes = pil_to_bytes(
            Image.fromarray(rgb_res),
            ext=ext,
            quality=95,
            infos=infos,
        )

        return Response(
            content=res_img_bytes,
            media_type=f"image/{ext}",
        )

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
