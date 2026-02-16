# 🐾 Animal Classifier - Django App

A Django web application that classifies images of dogs, cats, and birds using a pre-trained deep learning model.

## Features

- **Drag & Drop Upload**: Easy-to-use interface with drag-and-drop functionality
- **AI-Powered Classification**: Uses MobileNetV2 pre-trained model from TensorFlow
- **Real-time Predictions**: Instant classification results with confidence scores
- **Classification History**: View all previous classifications
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Project Structure

```
animalerie/
├── manage.py
├── requirements.txt
├── malla/                          # Main Django project
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── classifier/                     # Main Django app
│   ├── migrations/
│   ├── templates/
│   │   └── classifier/
│   │       ├── index.html         # Main upload interface
│   │       └── history.html       # Classification history
│   ├── __init__.py
│   ├── admin.py                   # Admin configuration
│   ├── apps.py
│   ├── forms.py                   # Django forms
│   ├── models.py                  # Database models
│   ├── ml_model.py                # AI classification logic
│   ├── urls.py                    # App URL routing
│   ├── views.py                   # View functions
│   └── tests.py
├── media/                         # Uploaded images storage
│   └── uploads/
└── static/                        # Static files (CSS, JS)
```

## Installation

### 1. Clone or Extract the Project

```bash
git clone https://github.com/ToroBaba04/AnimalClassifier.git
```

### 2. Create a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create a Superuser (Optional - for Admin Access)

```bash
python manage.py createsuperuser
```

### 6. Start the Development Server

```bash
python manage.py runserver
```

The application will be available at: `http://localhost:8000`

## Usage

### Main Interface

1. **Upload an Image**:
   - Click the upload area or drag and drop an image
   - Supported formats: JPG, PNG, GIF, WebP, etc.

2. **View Prediction**:
   - The AI model will analyze the image
   - You'll see the predicted animal (Dog, Cat, or Bird) and confidence percentage
   - A confidence bar shows how certain the model is

3. **View History**:
   - Click "View Classification History" link
   - See all previous classifications with timestamps

### Admin Panel

1. Access at: `http://localhost:8000/admin`
2. Login with your superuser credentials
3. View and manage all classifications in the database

## How It Works

### Image Classification Process

1. **User uploads image** → Frontend sends to server
2. **Image is saved** → Stored in `media/uploads/`
3. **Pre-trained model processes** → Uses MobileNetV2 from TensorFlow
4. **Predictions extracted** → Model returns top 20 predictions
5. **Animal type identified** → Searches predictions for dogs, cats, birds
6. **Result saved to database** → Stores prediction and confidence
7. **Result displayed** → User sees classification with confidence score

### Model Details

- **Architecture**: MobileNetV2 (lightweight, efficient)
- **Pre-trained on**: ImageNet dataset
- **Training**: No retraining needed - uses pre-trained weights
- **Supported classes**: Dogs, Cats, Birds (+ 1000+ ImageNet classes)
- **Input size**: 224×224 pixels (automatically resized)
- **Output**: Classification probability for each class

## API Endpoints

### Main Views

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Main upload interface |
| `/upload/` | POST | Handle image upload and classification |
| `/history/` | GET | View classification history |

### Upload Endpoint Details

**POST** `/upload/`

Request:
```
Content-Type: multipart/form-data
Parameters:
  - image: [image file]
  - csrfmiddlewaretoken: [CSRF token]
```

Response:
```json
{
  "success": true,
  "prediction": "dog",
  "confidence": "92.45%",
  "image_url": "/media/uploads/image_name.jpg",
  "id": 1
}
```

## Database Models

### Classification Model

```python
class Classification(models.Model):
    image          # ImageField - uploaded image file
    prediction     # CharField - 'dog', 'cat', or 'bird'
    confidence     # FloatField - prediction confidence (0-1)
    created_at     # DateTimeField - timestamp
```

## Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError: tensorflow

**Solution**:
```bash
pip install tensorflow --upgrade
```

#### 2. Image upload returns 400 error

**Solution**: Ensure the image is in a valid format (JPG, PNG, etc.)

#### 3. Permission denied on media folder

**Solution**:
```bash
chmod -R 755 media/
```

#### 4. Database errors

**Solution**: Run migrations again
```bash
python manage.py migrate
```

## Performance Tips

1. **Optimize Images**: Reduce image size before uploading for faster processing
2. **Clear Old Classifications**: Periodically clear old records from admin panel
3. **Use Production Server**: For production, use Gunicorn instead of development server:
   ```bash
   gunicorn malla.wsgi:application
   ```

## Development

### Run Tests

```bash
python manage.py test
```

### Create Django Shell

```bash
python manage.py shell
```

### Manage Database

```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations
```

## Future Enhancements

- [ ] Add model retraining capability
- [ ] Support for multiple model architectures
- [ ] Batch image processing
- [ ] API authentication and rate limiting
- [ ] Docker containerization
- [ ] Deployment to cloud (AWS, GCP, Azure)
- [ ] Mobile app wrapper
- [ ] WebSocket for real-time updates

## Security Considerations

- **CSRF Protection**: Enabled for all forms
- **File Validation**: Only images are accepted
- **Security Headers**: Configured in settings
- **SQL Injection**: Protected by Django ORM
- **XSS Protection**: Django template auto-escaping enabled

⚠️ **Production Deployment**: 
- Set `DEBUG = False` in settings.py
- Generate a new `SECRET_KEY`
- Configure `ALLOWED_HOSTS`
- Use HTTPS
- Set up proper media file serving (e.g., AWS S3)

## Technologies Used

- **Backend**: Django 4.2.7
- **ML Framework**: TensorFlow/Keras
- **Pre-trained Model**: MobileNetV2 ImageNet
- **Image Processing**: Pillow
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: SQLite (default, changeable)

## License

Open source project

## Support

For issues or questions, check:
1. Django documentation: https://docs.djangoproject.com/
2. TensorFlow documentation: https://www.tensorflow.org/
3. MobileNetV2 paper: https://arxiv.org/abs/1801.04381

---

**Created**: January 2026
**Version**: 1.0.0
