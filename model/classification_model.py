
from flask import make_response
from utils.helper_functions import analyse_image

class classification_model():
    def __init__(self):
        # connection establishment
        try:
            self.con = mysql.connector.connect(host="localhost", user="root", password="password", database="flask_tutorial")
            self.con.autocommit=True
            self.cur=self.con.cursor(dictionary=True) 
            print("Connection successfull")
        except:
            print("Error connectiing to the db")

    
    def classify_image(self, file, filePath):
        # classify image
        class_index = analyse_image(file)

        # class dictionary
        class_dictionary = { 0: 'early blight', 1: 'late blight', 2: 'septoria leaf spot', 3: 'healthy'}

        # Use the class index to look up the class name from the imported dictionary
        class_label = class_dictionary.get(class_index, 'Unknown Class')

        # Return a dictionary with the class name and other relevant information
        result = {'label': class_label, 'message': 'Image classified successfully'}

        # save the image
        # file.save(filePath)
        print(class_index)
        return result

    