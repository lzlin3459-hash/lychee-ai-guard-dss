import io
import requests
from PIL import Image

def test_api():
    # 制作一张假的 10x10 红光 JPEG
    img = Image.new('RGB', (10, 10), color = 'red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()

    url = 'http://127.0.0.1:5000/predict'
    files = {'file': ('test_red.jpg', img_byte_arr, 'image/jpeg')}
    
    try:
        r = requests.post(url, files=files)
        print(f"Status: {r.status_code}")
        print(f"Raw Text: {r.text[:500]}")
    except Exception as e:
        print(f"Failed to connect: {e}")

if __name__ == '__main__':
    test_api()
