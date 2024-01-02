import io
import os
from datetime import datetime
from PIL import Image 

from transformers import AutoImageProcessor
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
from ..utils import db


image_processor = AutoImageProcessor.from_pretrained("apple/mobilevitv2-1.0-imagenet1k-256")

class ClassificationResult(db.Model):

    __tablename__='classification_results'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_path = db.Column(db.String(255), nullable=False)
    result_value = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id=db.Column(db.Integer(), db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<Classifucation {self.id}>"


    @classmethod
    def generate_image_filepath(cls, file):
        """Generate a unique image filepath"""
        unique_file_name = str(datetime.now().timestamp()).replace(".", "")
        file_name_split = file.filename.split(".")
        file_ext = file_name_split[len(file_name_split)-1]
        file_path = f"api/uploads/{unique_file_name}.{file_ext}"

        return file_path

    
    @classmethod
    def get_image_class_name(cls, filepath):
        """Get the class of the image"""
        try:
            image = Image.open(filepath)

            # image processing
            transform = transforms.Compose([
                transforms.Resize((256,256)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

        
            image = transform(image).unsqueeze(0)
            image = image_processor(image, do_rescale=False, do_resize=False, return_tensors="pt")


            # Load the model and set it to evaluation
            model = torch.load('mobilevit_s_tomato.pth', map_location=torch.device('cpu'))
            model.eval()

            # make prediction
            with torch.no_grad():
                output = model(**image)

            logits = output.logits

            # Apply softmax to convert logits to probabilities
            probabilities = F.softmax(logits, dim=1)
            class_index = probabilities.argmax(dim=1).item()

            # get image class name
            class_dictionary = { 0: 'early blight', 1: 'late blight', 2: 'septoria leaf spot', 3: 'healthy'}
            class_name = class_dictionary.get(class_index, 'Unknown Class')

            return class_name, probabilities

        except Exception as e:
            print(f"Error classifying image: {e}")
            raise  # Re-raise the exception to propagate it to the caller


    def save(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def get_results_by_user_id(cls, user_id):
        result = cls.query.filter_by(user_id=user_id).all()
        return result


