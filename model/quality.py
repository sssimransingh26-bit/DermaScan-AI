from PIL import Image
import numpy as np

def check_image_quality(image_path):
    img=Image.open(image_path).convert('RGB')
    img_array=np.array(img)

    brightness=np.mean(img_array)
    if brightness<40:
        return False,"Image is too dark, please take photo in better lighting"
    if brightness>220:
        return False,"Image is too bright or overexposed. Please take in natural light"
    
    return True, "Image quality is good."