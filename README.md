## A Simple MobileViT Image Classification API

### Overview

This Flask application serves as an API for image classification using a pre-trained deep learning model, MobileViT. It allows users to upload tomato leaf images and receive predictions about the class of the image, such as whether it depicts a type of plant disease (early blight, late blight or septoria leaf spot) or is considered healthy.

### Components

#### Controller (`imageClassificationController.py`)

- **`get_image_class` Endpoint:**
  - **HTTP Method:** POST
  - **Path:** `/classify-image`
  - **Description:** Accepts an image file upload and returns the predicted class label along with additional information.

- **`get_uploaded_image` Endpoint:**
  - **HTTP Method:** GET
  - **Path:** `/uploads/<filename>`
  - **Description:** Retrieves and serves a previously uploaded image based on the provided filename.

#### Model (`imageClassification.py`)

- **`imageClassification` Class:**
  - **Initialization:** Establishes a connection to a MySQL database for storing classification results.
  - **Methods:**
    - `classify_image(filepath)`: Utilizes a pre-trained deep learning model to classify an image based on the provided file path.
    - `image_class(filepath)`: Invokes `classify_image` and saves the classification result to the database, returning a response to the user.
    - `save_classification_result(filepath, result)`: Inserts the classification result and associated image details into the MySQL database.

### Setup and Dependencies

1. **Flask Application (`app` folder):**
   - Install the required Python packages listed in `requirements.txt`.
   - Run the Flask application using the command: `flask run`.

2. **Deep Learning Model:**
   - A pre-trained deep learning model (`mobilevit_s_tomato.pth`) for image classification should be available in the application directory.

3. **Database Configuration:**
   - Set up a MySQL database with the name "tomato_disease_classification" on the local server.
   - Configure the database connection parameters (host, user, password) in the `imageClassification` class constructor.

### Usage

1. **Uploading an Image:**
   - Send a POST request to `/classify-image` with an image file attached.

2. **Retrieving an Uploaded Image:**
   - Access the image by sending a GET request to `/uploads/<filename>` with the filename received in the response from the `/classify-image` endpoint.

### Error Handling

- The API provides informative error responses for cases such as missing files, invalid file extensions, and internal server errors.
