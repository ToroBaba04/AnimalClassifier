# 🎯 Quick Start: Model Prediction Setup

This guide will help you get predictions running quickly with your .h5 model.

## ⚡ 5-Minute Setup

### Step 1: Place Your Model File

Copy your trained model to the `classifier/model/` folder:

```bash
# From your project root
mkdir -p classifier/model
cp /path/to/CatDogBird_model.h5 classifier/model/
```

**Accepted filenames:**
- `CatDogBird_model.h5` ✓
- `CatDogBird_model_Adv.h5` ✓
- `model.h5` ✓
- `ANN_model.weights.h5` (weights only) ✓

### Step 2: Test the Setup

```bash
# From project root
python predict.py /path/to/test/dog.jpg
```

### Step 3: Use in Django

In your views:

```python
from classifier.ml_model import classify_image

result = classify_image('media/uploads/test.jpg')
# Returns: {'animal': 'dog', 'confidence': 0.95}
```

---

## 🚀 Usage Methods

### Method 1: Command Line

```bash
# Single image
python predict.py /path/to/image.jpg

# Batch process folder
python predict.py /path/to/images/folder/
```

### Method 2: Python Script

```python
from classifier.ml_model import classify_image

result = classify_image('path/to/image.jpg')
print(f"{result['animal']}: {result['confidence']:.2%}")
```

### Method 3: Interactive Notebook

Open and run `Model_Prediction.ipynb` for interactive predictions with visualizations.

### Method 4: Django Integration

```python
# views.py
from classifier.ml_model import classify_image
from django.shortcuts import render

def predict_view(request):
    if request.FILES['image']:
        image = request.FILES['image']
        # Save to temporary location
        image_path = f"media/temp/{image.name}"
        
        # Get prediction
        result = classify_image(image_path)
        
        return render(request, 'result.html', {
            'animal': result['animal'],
            'confidence': f"{result['confidence']:.2%}"
        })
```

---

## 📊 Output Format

All methods return:

```python
{
    'animal': 'dog',           # 'bird', 'cat', or 'dog'
    'confidence': 0.95         # 0.0 to 1.0
}
```

---

## ❓ Troubleshooting

### "No model files found"

**Solution:** Check that your .h5 file is in `classifier/model/`

```bash
ls -la classifier/model/
# Should show your .h5 file
```

### "Failed to load model"

**Possible causes:**
1. File is corrupted
2. TensorFlow version mismatch
3. File is not a valid Keras model

**Solution:**
```bash
# Verify with TensorFlow
python -c "import tensorflow as tf; model = tf.keras.models.load_model('classifier/model/CatDogBird_model.h5')"
```

### "Out of memory" error

**Solution:** Process images one at a time instead of batch

### Model loads but predictions are wrong

**Check:**
1. Image must be resized to 224x224 (automatic in our code)
2. Ensure image quality is similar to training data
3. Try with a known test image first

---

## 📚 Documentation Files

- **[MODEL_SETUP.md](MODEL_SETUP.md)** - Detailed setup guide
- **[Model_Prediction.ipynb](Model_Prediction.ipynb)** - Interactive notebook
- **[predict.py](predict.py)** - Standalone prediction script

---

## 🔧 Environment Setup

### Option A: Use existing environment

If you already have TensorFlow installed with compatible versions, you can use the classifier directly.

### Option B: Create new environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements-prediction.txt
```

### Check environment

```bash
python -c "import tensorflow as tf; print(f'TensorFlow: {tf.__version__}')"
```

---

## 📝 Model Information

- **Architecture:** EfficientNetB0
- **Classes:** Bird, Cat, Dog
- **Input Size:** 224 × 224 × 3 (RGB)
- **Input Format:** JPEG, PNG, BMP, etc.
- **Output:** Probability scores for each class

---

## 💡 Tips

1. **Batch Processing:** Use `python predict.py folder/` for multiple images
2. **Visualization:** Use the Jupyter notebook to see confidence bars
3. **Integration:** Import `classify_image` in any Python script
4. **Performance:** Model requires ~2GB RAM for inference

---

## 🎓 Example: Train → Save → Load → Predict

From your Kaggle notebook:

```python
# Training (you already did this)
model.save('saved_model/CatDogBird_model.h5')

# You downloaded the .h5 file
# Place it in: classifier/model/CatDogBird_model.h5

# Now use it (in AnimalClassifier)
from classifier.ml_model import classify_image
result = classify_image('media/uploads/my_image.jpg')
print(result)
```

That's it! Your model is ready to make predictions. 🎉
