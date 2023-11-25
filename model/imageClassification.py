import io
import os
import torch
from PIL import Image 
import mysql.connector
from flask import make_response
from transformers import AutoImageProcessor
import torchvision.transforms as transforms
from utils.helper_functions import generateImageFilepath
image_processor = AutoImageProcessor.from_pretrained("apple/mobilevitv2-1.0-imagenet1k-256")


class imageClassification():
    def __init__(self):
        # connection establishment
        try:
            self.con = mysql.connector.connect(host="localhost", user="root", password="password", database="tomato_disease_classification")
            self.con.autocommit=True
            self.cur=self.con.cursor(dictionary=True) 
            print("connection successfull")
        except Exception as e:
            print(f"Error connecting to the database: {e}")

    
    def classifyImage(self, filepath):
        try:
            # Use PIL to open the image directly from the file path
            image = Image.open(filepath)

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
        
        except Exception as e:
            print(f"Error classifying image: {e}")
            raise  # Re-raise the exception to propagate it to the caller

    

    def imageClass(self, filepath):
        try:
            # get image class
            class_index = self.classifyImage(filepath);

            # class dictionary
            class_dictionary = { 0: 'early blight', 1: 'late blight', 2: 'septoria leaf spot', 3: 'healthy'}

            # get class label
            class_label = class_dictionary.get(class_index, 'Unknown Class')

            # save classification result
            success = self.saveClassificationResult(filepath, class_label)
            
            # Extract the file name from the path
            filename = os.path.basename(filepath)

            # return result to user based on the success of saving
            if success:
                result = {'label': class_label, 'filename': filename}
            else:
                result = {'message': 'Error saving classification result'}

            return result
        except Exception as e:
            print(f"error processing image: {e}")
            return {'message': 'error processing image'}
    


    def saveClassificationResult(self, filepath, result):
        try: 
            # Insert the classification result into the 'result' table
            query = "INSERT INTO classification_result (result) VALUES (%s)"
            self.cur.execute(query, (result,))
            result_id = self.cur.lastrowid  # Get the last inserted result_id

            # Insert the image details into the 'image' table
            query = "INSERT INTO image (image_path, result_id) VALUES (%s, %s)"
            self.cur.execute(query, (filepath, result_id))

            return True
        except Exception as e:
            print(f"Error saving classification result: {e}")
            return False