from datetime import datetime
import io
import torch
from PIL import Image 
import torchvision.transforms as transforms
from transformers import AutoImageProcessor
image_processor = AutoImageProcessor.from_pretrained("apple/mobilevitv2-1.0-imagenet1k-256")



def generate_image_filepath(file):
    uniqueFileName = str(datetime.now().timestamp()).replace(".", "") # generate unique image name
    fileNameSplit = file.filename.split(".")
    fileExt = fileNameSplit[len(fileNameSplit)-1]
    filePath = f"uploads/{uniqueFileName}.{fileExt}"

    return filePath


def analyse_image(file_storage):
    # Read the content of the file storage as bytes
    input_image = file_storage.read()

    # Use io.BytesIO to create a bytes-like object
    image = Image.open(io.BytesIO(input_image))

    # image processing 
    transform = transforms.Compose([
        transforms.Resize((256,256)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

    
    image = transform(image).unsqueeze(0)
    image = image_processor(image, do_rescale=False, do_resize=False, return_tensors="pt")

    # load imodel
    model = torch.load('mobilevit_s_tomato.pth', map_location=torch.device('cpu'))

    # set model to evaluation mode
    model.eval()

    # make prediction
    with torch.no_grad():
        output = model(**image)

    logits = output.logits

    # single class label
    class_index = logits.argmax(dim=1).item()

    return class_index


