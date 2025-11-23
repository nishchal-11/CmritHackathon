# Models Directory

## 📦 Precomputed Masks (`precomputed/`)

After running the Google Colab notebook, extract the ZIP file here:

```
precomputed/
├── node_1_indiranagar/
│   ├── metadata.json
│   ├── frame_00000_mask.png
│   ├── frame_00000_overlay.png
│   └── ...
├── node_2_koramangala/
├── node_3_silkboard/
└── hub_mgroad/
```

The backend will load these pre-computed results for instant demo playback.

## 🧠 Model Checkpoints

If running SAM 2 or Real-ESRGAN locally, place model weights here:
- `sam2_hiera_large.pt` (if using SAM 2 locally)
- `RealESRGAN_x4plus.pth` (if using Real-ESRGAN locally)

**Note**: For hackathon demo, use precomputed results from Colab to avoid GPU requirements.
