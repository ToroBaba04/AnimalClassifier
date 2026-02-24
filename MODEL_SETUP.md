# Model Setup Guide

## Directory Structure

The model files should be placed in the `classifier/model/` directory:

```
AnimalClassifier/
├── classifier/
│   ├── model/
│   │   ├── CatDogBird_model.h5          # Option 1: Full model
│   │   ├── CatDogBird_model_Adv.h5      # Option 1: Full model (advanced)
│   │   └── ANN_model.weights.h5         # Option 2: Weights only
│   ├── ml_model.py
│   ├── views.py
│   └── ...
```

## Placing Your Model Files

### Option 1: Use the Full Model (Recommended)
1. Save your model from Kaggle:
```python
model.save('saved_model/CatDogBird_model.h5')
```

2. Place `CatDogBird_model.h5` in `classifier/model/` directory

### Option 2: Use Weights Only
1. Save your model weights from Kaggle:
```python
model.save_weights('saved_model/ANN_model.weights.h5')
```

2. Place `ANN_model.weights.h5` in `classifier/model/` directory

## Using the Model in Your Django Application

### Basic Usage

```python
from classifier.ml_model import classify_image

# Classify an image
result = classify_image('/path/to/image.jpg')
print(result)  
# Output: {'animal': 'dog', 'confidence': 0.95}
```

### In Views

```python
from django.shortcuts import render
from classifier.ml_model import classify_image

def predict_view(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        # Save temporarily or get path
        result = classify_image(image_path)
        
        return render(request, 'result.html', {
            'animal': result['animal'],
            'confidence': f"{result['confidence']:.2%}"
        })
```

## Model Classes

The model recognizes three classes:
- **bird**: Birds of various species
- **cat**: Domestic and wild cats
- **dog**: Domestic and wild dogs

## Input Requirements

- **Image Size**: 224x224 pixels (automatically resized)
- **Color Mode**: RGB
- **Format**: JPG, PNG, BMP, etc. (any format PIL can read)

## Preprocessing Details

The model uses EfficientNetB0 preprocessing:
- Resizes images to 224x224
- Applies EfficientNetB0 preprocessing
- Normalizes pixel values appropriately

## Confidence Score

The confidence score is a float between 0 and 1:
- **0.95** = 95% confidence
- **0.75** = 75% confidence
- **0.33** = Low confidence (ambiguous image)

## Troubleshooting

### "No model files found"
- Ensure you've placed the .h5 file in `classifier/model/`
- Check the filename matches uno of: `CatDogBird_model.h5`, `CatDogBird_model_Adv.h5`, `ANN_model.weights.h5`

### "Failed to load model"
- Ensure the .h5 file is a valid Keras model
- Check file is not corrupted (try opening in another system)
- Verify TensorFlow version matches training environment

### "OutOfMemory" error
- Model requires ~2GB RAM for inference
- Consider reducing batch size if processing multiple images

## Model Architecture

```
Input (224, 224, 3)
    ↓
EfficientNetB0 (pre-trained on ImageNet)
    ↓
Dense(132, relu)
    ↓
Dense(64, relu)
    ↓
Dense(3, softmax)  ← Output probabilities for bird/cat/dog
```

## Training Details (Reference)

- **Base Model**: EfficientNetB0 (pre-trained on ImageNet)
- **Loss Function**: Categorical Crossentropy
- **Optimizer**: Adam (learning_rate=0.001)
- **Image Input Size**: 224x224
- **Training Epochs**: 15
- **Batch Size**: 16
- **Dataset**: High-resolution cat, dog, bird images (~13,000 images)
