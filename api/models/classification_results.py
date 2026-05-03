from PIL import Image
from transformers import AutoImageProcessor
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms


image_processor = AutoImageProcessor.from_pretrained("apple/mobilevitv2-1.0-imagenet1k-256")


def get_image_class_name(image_source):
    image = Image.open(image_source).convert("RGB")

    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    image = transform(image).unsqueeze(0)
    image = image_processor(image, do_rescale=False, do_resize=False, return_tensors="pt")

    model = torch.load('mobilevit_s_tomato.pth', map_location=torch.device('cpu'), weights_only=False)
    model.eval()

    with torch.no_grad():
        output = model(**image)

    probabilities = F.softmax(output.logits, dim=1)
    class_index = probabilities.argmax(dim=1).item()

    class_dictionary = {0: 'early blight', 1: 'late blight', 2: 'septoria leaf spot', 3: 'healthy'}
    return class_dictionary.get(class_index, 'Unknown Class'), probabilities
