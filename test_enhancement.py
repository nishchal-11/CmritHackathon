# Test Image Enhancement Endpoint
# Creates a sample image and tests the enhancement

from PIL import Image, ImageDraw, ImageFont
import requests

# Create a small test image (simulating low-res surveillance footage)
img = Image.new('RGB', (320, 240), color='#1a1a1a')
draw = ImageDraw.Draw(img)

# Draw some test content
draw.rectangle([50, 50, 270, 190], outline='#00ff41', width=3)
draw.text((100, 100), "Test Image", fill='#00ff41')
draw.ellipse([140, 140, 180, 180], fill='#ff4444')

# Save test image
test_path = "test_surveillance.png"
img.save(test_path)

print(f"Created test image: {test_path}")
print(f"Size: {img.size}")

# Upload to enhancement API
url = "http://127.0.0.1:8000/api/enhance/upload?scale=2"

with open(test_path, 'rb') as f:
    files = {'file': ('test_surveillance.png', f, 'image/png')}
    response = requests.post(url, files=files)

if response.status_code == 200:
    result = response.json()
    print("\n✅ Enhancement successful!")
    print(f"   Original: {result['original_size']}")
    print(f"   Enhanced: {result['enhanced_size']}")
    print(f"   Scale: {result['scale_factor']}")
    print(f"   Technique: {result['technique']}")
    print(f"\n   View enhanced image at:")
    print(f"   http://127.0.0.1:8000{result['enhanced_path']}")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
