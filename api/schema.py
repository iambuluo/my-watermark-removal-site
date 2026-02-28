from typing import Optional
from pydantic import BaseModel

class InpaintRequest(BaseModel):
    image: str
    mask: str
    ldm_steps: int = 50
    ldm_sampler: str = "plms"
    zits_wireframe: bool = True
    hd_strategy: str = "Original"
    hd_strategy_crop_margin: int = 128
    hd_strategy_crop_trigger_size: int = 2048
    hd_strategy_resize_limit: int = 2048
    prompt: str = ""
    negative_prompt: str = ""
    use_croper: bool = False
    croper_x: int = 0
    croper_y: int = 0
    croper_height: int = 512
    croper_width: int = 512
    sd_scale: float = 1.0
    sd_mask_blur: int = 5
    sd_strength: float = 0.75
    sd_steps: int = 50
    sd_guidance_scale: float = 7.5
    sd_sampler: str = "ddim"
    sd_seed: int = 42
    sd_match_histograms: bool = False
    cv2_flag: str = "INPAINT_NS"
    cv2_radius: int = 4
    paint_by_example_example_image: Optional[str] = None
    p2p_image_guidance_scale: float = 1.5
    enable_controlnet: bool = False
    controlnet_method: Optional[str] = None
    controlnet_conditioning_scale: float = 0.4
    control_previous_step_img: Optional[str] = None
    enable_brushnet: bool = False
    brushnet_method: Optional[str] = None
    brushnet_conditioning_scale: float = 1.0
    enable_powerpaint_v2: bool = False
    powerpaint_task: str = "text-guided"
    sd_lcm_lora: bool = False
