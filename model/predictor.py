import torch
torch.set_num_threads(1)
from torchvision import transforms
from PIL import Image
import torch.nn as nn
import timm


LABELS=['Melanocytic nevi',
    'Melanoma',
    'Benign keratosis',
    'Basal cell carcinoma',
    'Actinic keratosis',
    'Vascular lesion',
    'Dermatofibroma'
    ]

#loading pre trained model
def load_model():
    model=timm.create_model('efficientnet_b0',pretrained=True, num_classes=7)
    model.eval()
    return model

def transform_image(image_path):#preprocess uploaded image before prediction
    transform=transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
        ])
    image = Image.open(image_path).convert('RGB')
    return transform(image).unsqueeze(0)
    

def predict(image_path):
    model = load_model()
    tensor = transform_image(image_path)
    
    with torch.no_grad():#only predicting not training
        outputs = model(tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        confidence, predicted = torch.max(probabilities, 0)
    
    return {
        'condition': LABELS[predicted.item()],
        'confidence': round(confidence.item() * 100, 2)
    }