"""
Real-ESRGAN GAN-based image enhancement
Uses the actual Real-ESRGAN model from tools/Real-ESRGAN
"""
from fastapi import APIRouter, File, UploadFile, HTTPException
from pathlib import Path
import shutil
import sys
from typing import Dict, Any
import uuid

router = APIRouter()

# Path to assets and Real-ESRGAN
ASSETS_PATH = Path(__file__).parent.parent.parent.parent / "assets"
ENHANCED_PATH = ASSETS_PATH / "enhanced"
ENHANCED_PATH.mkdir(parents=True, exist_ok=True)

REALESRGAN_PATH = Path(__file__).parent.parent.parent.parent / "tools" / "Real-ESRGAN"
sys.path.insert(0, str(REALESRGAN_PATH))

# Try to import Real-ESRGAN components
REALESRGAN_AVAILABLE = False
RRDBNet = None
RealESRGANer = None
SRVGGNetCompact = None

try:
    import cv2
    import numpy as np
    from basicsr.archs.rrdbnet_arch import RRDBNet
    from realesrgan import RealESRGANer
    from realesrgan.archs.srvgg_arch import SRVGGNetCompact
    REALESRGAN_AVAILABLE = True
except (ImportError, ModuleNotFoundError) as e:
    # Silently handle missing dependencies - feature will be disabled
    REALESRGAN_AVAILABLE = False
    pass


@router.post("/gan")
async def enhance_with_realesrgan(file: UploadFile = File(...), model: str = "RealESRGAN_x4plus") -> Dict[str, Any]:
    """
    Enhance image using actual Real-ESRGAN GAN model
    
    Models available:
    - RealESRGAN_x4plus (default): Best quality, 4x upscaling
    - RealESRGAN_x2plus: 2x upscaling, faster
    - realesr-general-x4v3: General purpose, smaller model
    
    Args:
        file: Image file to enhance
        model: Model to use
    
    Returns:
        Enhanced image with GAN processing
    """
    if not REALESRGAN_AVAILABLE:
        raise HTTPException(
            status_code=503, 
            detail="Real-ESRGAN not installed. Install with: pip install basicsr realesrgan opencv-python"
        )
    
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Generate unique ID
    job_id = str(uuid.uuid4())[:8]
    
    # Save original
    original_filename = f"{job_id}_original_{file.filename}"
    original_path = ENHANCED_PATH / original_filename
    
    with open(original_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Setup Real-ESRGAN model
        if model == 'RealESRGAN_x4plus':
            netscale = 4
            model_arch = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
            model_path = REALESRGAN_PATH / 'weights' / 'RealESRGAN_x4plus.pth'
        elif model == 'RealESRGAN_x2plus':
            netscale = 2
            model_arch = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
            model_path = REALESRGAN_PATH / 'weights' / 'RealESRGAN_x2plus.pth'
        elif model == 'realesr-general-x4v3':
            netscale = 4
            model_arch = SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=32, upscale=4, act_type='prelu')
            model_path = REALESRGAN_PATH / 'weights' / 'realesr-general-x4v3.pth'
        else:
            raise HTTPException(status_code=400, detail=f"Unknown model: {model}")
        
        # Initialize upsampler
        upsampler = RealESRGANer(
            scale=netscale,
            model_path=str(model_path),
            model=model_arch,
            tile=0,
            tile_pad=10,
            pre_pad=0,
            half=False  # Use FP32 for compatibility
        )
        
        # Read image
        img = cv2.imread(str(original_path), cv2.IMREAD_UNCHANGED)
        
        # Enhance with Real-ESRGAN
        output, _ = upsampler.enhance(img, outscale=netscale)
        
        # Save enhanced image
        enhanced_filename = f"{job_id}_realesrgan_{model}_{file.filename}"
        enhanced_path = ENHANCED_PATH / enhanced_filename
        cv2.imwrite(str(enhanced_path), output)
        
        # Get image dimensions
        original_h, original_w = img.shape[:2]
        enhanced_h, enhanced_w = output.shape[:2]
        
        return {
            "status": "success",
            "job_id": job_id,
            "message": f"Enhanced with Real-ESRGAN {model}",
            "original_path": f"/static/assets/enhanced/{original_filename}",
            "enhanced_path": f"/static/assets/enhanced/{enhanced_filename}",
            "original_size": f"{original_w}x{original_h}",
            "enhanced_size": f"{enhanced_w}x{enhanced_h}",
            "scale_factor": f"{netscale}x",
            "model": model,
            "technique": "Real-ESRGAN GAN-based Super Resolution",
            "gan_type": "Generative Adversarial Network"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Real-ESRGAN enhancement failed: {str(e)}")


@router.post("/gan-variations")
async def generate_gan_variations(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Generate multiple variations using different Real-ESRGAN models
    
    Creates 3 variations:
    1. RealESRGAN_x4plus (Best quality)
    2. RealESRGAN_x2plus (Faster processing)
    3. realesr-general-x4v3 (Balanced)
    
    Args:
        file: Image file to enhance
    
    Returns:
        Multiple GAN-enhanced variations
    """
    if not REALESRGAN_AVAILABLE:
        raise HTTPException(
            status_code=503, 
            detail="Real-ESRGAN not installed. Install with: pip install basicsr realesrgan opencv-python"
        )
    
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    job_id = str(uuid.uuid4())[:8]
    
    # Save original
    original_filename = f"{job_id}_original_{file.filename}"
    original_path = ENHANCED_PATH / original_filename
    
    with open(original_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    img = cv2.imread(str(original_path), cv2.IMREAD_UNCHANGED)
    original_h, original_w = img.shape[:2]
    
    variations = []
    models_config = [
        ('RealESRGAN_x4plus', 4, RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4), 'High Quality 4x'),
        ('RealESRGAN_x2plus', 2, RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2), 'Fast 2x'),
        ('realesr-general-x4v3', 4, SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=32, upscale=4, act_type='prelu'), 'General Purpose 4x'),
    ]
    
    try:
        for model_name, scale, model_arch, description in models_config:
            model_path = REALESRGAN_PATH / 'weights' / f'{model_name}.pth'
            
            # Skip if model weights don't exist
            if not model_path.exists():
                continue
            
            upsampler = RealESRGANer(
                scale=scale,
                model_path=str(model_path),
                model=model_arch,
                tile=0,
                tile_pad=10,
                pre_pad=0,
                half=False
            )
            
            output, _ = upsampler.enhance(img, outscale=scale)
            
            enhanced_filename = f"{job_id}_{model_name}_{file.filename}"
            enhanced_path = ENHANCED_PATH / enhanced_filename
            cv2.imwrite(str(enhanced_path), output)
            
            enhanced_h, enhanced_w = output.shape[:2]
            
            variations.append({
                "name": model_name,
                "path": f"/static/assets/enhanced/{enhanced_filename}",
                "technique": "Real-ESRGAN GAN Architecture",
                "description": description,
                "size": f"{enhanced_w}x{enhanced_h}",
                "scale": f"{scale}x",
                "angle": "GAN Enhanced"
            })
        
        if not variations:
            raise Exception("No Real-ESRGAN model weights found. Download models first.")
        
        return {
            "status": "success",
            "job_id": job_id,
            "message": f"Generated {len(variations)} Real-ESRGAN variations",
            "original_path": f"/static/assets/enhanced/{original_filename}",
            "original_size": f"{original_w}x{original_h}",
            "total_variations": len(variations),
            "variations": variations,
            "technique": "Real-ESRGAN Multi-Model GAN Processing"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GAN variation generation failed: {str(e)}")


@router.get("/status")
async def realesrgan_status() -> Dict[str, Any]:
    """Check Real-ESRGAN availability and installed models"""
    
    if not REALESRGAN_AVAILABLE:
        return {
            "available": False,
            "message": "Real-ESRGAN not installed",
            "install_command": "pip install basicsr realesrgan opencv-python torch torchvision"
        }
    
    weights_path = REALESRGAN_PATH / 'weights'
    available_models = []
    
    model_files = [
        'RealESRGAN_x4plus.pth',
        'RealESRGAN_x2plus.pth',
        'realesr-general-x4v3.pth',
        'RealESRGAN_x4plus_anime_6B.pth'
    ]
    
    for model_file in model_files:
        if (weights_path / model_file).exists():
            available_models.append(model_file)
    
    return {
        "available": True,
        "message": "Real-ESRGAN is operational",
        "gan_type": "Generative Adversarial Network",
        "technique": "Real-ESRGAN Super Resolution",
        "weights_path": str(weights_path),
        "available_models": available_models,
        "total_models": len(available_models)
    }
