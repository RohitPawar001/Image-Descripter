import torch
from torchvision import models, transforms
from PIL import Image
import json
import requests
from io import BytesIO

class ImagePredicator:
    
    model = None
    class_idx = None
    
    @classmethod
    def _load_model(cls):
        if cls.model is None:
            cls.model = models.inception_v3(pretrained=True)
            cls.model.eval() 
        return cls.model
    
    @classmethod
    def _load_class_index(cls):
        if cls.class_idx is None:
            try:
                with open('imagenet_class_index.json') as f:
                    cls.class_idx = json.load(f)
            except FileNotFoundError:
                url = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
                response = requests.get(url)
                class_names = response.json()
                cls.class_idx = {str(i): [str(i), name] for i, name in enumerate(class_names)}
                with open('imagenet_class_index.json', 'w') as f:
                    json.dump(cls.class_idx, f)
        return cls.class_idx
    
    @classmethod
    def predict_image(cls, image, top_k=1):
        # Load model
        model = cls._load_model()
        
        
        preprocess = transforms.Compose([
            transforms.Resize(299),  
            transforms.CenterCrop(299),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
       
        input_tensor = preprocess(image)
        input_batch = input_tensor.unsqueeze(0)  
        
       
        if torch.cuda.is_available():
            input_batch = input_batch.to('cuda')
            model.to('cuda')
        
        
        with torch.no_grad():
            output = model(input_batch)
        
        
        probabilities = torch.nn.functional.softmax(output[0], dim=0)
        
        
        top_probs, top_indices = torch.topk(probabilities, top_k)
        
        
        class_idx = cls._load_class_index()
        
        
        results = []
        for i in range(top_k):
            idx = top_indices[i].item()
            results.append({
                'class': class_idx[str(idx)][1],
                'probability': top_probs[i].item()
            })
        
        return results