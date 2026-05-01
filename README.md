# Tomato Disease Detection API

A Flask REST API for detecting tomato leaf diseases from images using a fine-tuned MobileViT model. The model classifies tomato leaf images into four categories: Early Blight, Late Blight, Septoria Leaf Spot, and Healthy.

## Model

The API uses a MobileViT-S model (`mobilevit_s_tomato.pth`) fine-tuned on tomato disease data, with image preprocessing via Apple's `mobilevitv2-1.0-imagenet1k-256` processor.

**Supported classes:**

| Label | Description |
|-------|-------------|
| `early blight` | Caused by *Alternaria solani* fungus |
| `late blight` | Caused by *Phytophthora infestans* |
| `septoria leaf spot` | Caused by *Septoria lycopersici* fungus |
| `healthy` | No disease detected |

## Requirements

- Python 3.11+
- See `requirements.txt` for full dependency list

## Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
FLASK_DEBUG=True
```

## Running the API

```bash
flask --app app run
```

The API will be available at `http://127.0.0.1:5000`.  
Interactive Swagger UI: `http://127.0.0.1:5000/`

## Database Migrations

```bash
flask db init      # first time only
flask db migrate
flask db upgrade
```

---

## Authentication

All classification endpoints require a JWT access token. Include it in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

Access tokens expire after **5 minutes**. Use the refresh token (valid for **20 minutes**) to obtain a new access token.

---

## API Reference

### Auth

#### `POST /auth/register`

Create a new user account.

**Request body:**
```json
{
  "firstname": "Jane",
  "lastname": "Doe",
  "username": "janedoe",
  "password": "secret"
}
```

**Responses:**

| Status | Description |
|--------|-------------|
| `201 Created` | User created successfully |
| `409 Conflict` | Username already exists |

---

#### `POST /auth/login`

Authenticate and receive JWT tokens.

**Request body:**
```json
{
  "username": "janedoe",
  "password": "secret"
}
```

**Response `200 OK`:**
```json
{
  "access_token": "<jwt_access_token>",
  "refresh_token": "<jwt_refresh_token>",
  "user_name": "janedoe",
  "id": 1
}
```

| Status | Description |
|--------|-------------|
| `200 OK` | Login successful |
| `401 Unauthorized` | Invalid credentials |

---

#### `GET /auth/refresh`

Obtain a new access token using a refresh token.

**Headers:**
```
Authorization: Bearer <refresh_token>
```

**Response `200 OK`:**
```json
{
  "access_token": "<new_jwt_access_token>"
}
```

---

### Classification

#### `POST /classification/classify`

Upload a tomato leaf image for disease classification. Requires a valid access token.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Form data:**

| Field | Type | Description |
|-------|------|-------------|
| `image` | file | Tomato leaf image (`.jpg`, `.jpeg`, or `.png`) |

**Response `200 OK`:**
```json
{
  "label": "early blight",
  "image_url": "http://127.0.0.1:5000/api/uploads/1703704042311672.jpg",
  "label_probabilities": {
    "Early Blight": 0.8731,
    "Late Blight": 0.0423,
    "Septoria Leaf Spot": 0.0612,
    "Healthy": 0.0234
  }
}
```

| Status | Description |
|--------|-------------|
| `200 OK` | Classification successful |
| `400 Bad Request` | No file provided or invalid file type |
| `401 Unauthorized` | Missing or invalid token |
| `500 Internal Server Error` | Model inference error |

---

#### `GET /classification/classification_results/<user_id>`

Retrieve paginated classification history for a user. Requires a valid access token.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query parameters:**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `page` | `1` | Page number |
| `per_page` | `2` | Results per page |

**Response `200 OK`:**
```json
{
  "results": [
    {
      "image_url": "http://127.0.0.1:5000/api/uploads/1703704042311672.jpg",
      "result_value": "early blight",
      "timestamp": "2024-01-15T10:30:00"
    }
  ],
  "total_pages": 5
}
```

| Status | Description |
|--------|-------------|
| `200 OK` | Results returned |
| `204 No Content` | No results for this user |
| `404 Not Found` | User does not exist |

---

#### `GET /classification/image/<image_file_name>`

Retrieve a previously uploaded image by filename. Does not require authentication.

**Example:**
```
GET /classification/image/1703704042311672.jpg
```

| Status | Description |
|--------|-------------|
| `200 OK` | Image returned |
| `404 Not Found` | Image not found |

---

## Project Structure

```
mobilevit-flask-api/
├── app.py                      # Application entry point
├── mobilevit_s_tomato.pth      # Fine-tuned MobileViT model
├── requirements.txt
├── .env
├── api/
│   ├── __init__.py             # App factory
│   ├── auth/
│   │   └── views.py            # Register, login, refresh endpoints
│   ├── classification/
│   │   └── views.py            # Classify, history, image endpoints
│   ├── config/
│   │   └── config.py           # Dev/prod/test config
│   ├── models/
│   │   ├── users.py
│   │   └── classification_results.py
│   ├── uploads/                # Stored uploaded images
│   └── utils/
│       └── __init__.py         # SQLAlchemy db instance
└── instance/
    └── db.sqlite3              # SQLite database
```
