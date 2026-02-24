"""
Image classification using custom EfficientNetB0 model
Trained on high-resolution cat, dog, and bird images
Model architecture: EfficientNetB0 + Dense(132) + Dense(64) + Dense(3)
"""
import os
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.optimizers import Adam


class AnimalClassifier:
    """Custom trained EfficientNetB0 model for classifying animals in images"""
    
    def __init__(self):
        """Initialize the custom trained model"""
        # Get the model path relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_dir = os.path.join(current_dir, 'model')
        
        # Try to load from full model file first, then from weights
        self.model = self._load_model(model_dir)
        self.classes = ['bird', 'cat', 'dog']  # Class order from training
        self.img_size = (224, 224)
    
    def _load_model(self, model_dir):
        """
        Attempt to load model from .h5 file or weights file
        
        Args:
            model_dir: Path to model directory
            
        Returns:
            Compiled Keras model
        """
        # Try loading from full model files first
        model_candidates = [
            'CatDogBird_model.h5',
            'CatDogBird_model_Adv.h5',
            'model.h5'
        ]
        
        for model_name in model_candidates:
            model_path = os.path.join(model_dir, model_name)
            if os.path.exists(model_path):
                try:
                    print(f"Loading model from {model_path}...")
                    model = tf.keras.models.load_model(model_path)
                    print(f"✓ Model loaded successfully from {model_path}")
                    return model
                except Exception as e:
                    print(f"Failed to load from {model_path}: {e}")
                    continue
        
        # If full model not found, try to load from weights
        weights_path = os.path.join(model_dir, 'ANN_model.weights.h5')
        if os.path.exists(weights_path):
            try:
                print(f"Loading model architecture and weights from {weights_path}...")
                model = self._build_model()
                model.load_weights(weights_path)
                print(f"✓ Model loaded successfully from {weights_path}")
                return model
            except Exception as e:
                print(f"Failed to load from weights: {e}")
        
        # If we get here, no model files were found
        raise FileNotFoundError(
            f"No model files found in {model_dir}\n"
            f"Please place one of the following in the classifier/model/ directory:\n"
            f"  - Full model: CatDogBird_model.h5 or CatDogBird_model_Adv.h5\n"
            f"  - Weights only: ANN_model.weights.h5 (will rebuild architecture)\n"
        )
    
    def _build_model(self):
        """Rebuild the EfficientNetB0 architecture used during training"""
        # Create base EfficientNetB0 model (same as Kaggle training)
        base_model = EfficientNetB0(
            include_top=False,
            weights='imagenet',
            input_shape=(224, 224, 3),
            pooling='max'
        )
        # Keep trainable=True as used in training
        base_model.trainable = True
        
        # Build the exact architecture from training
        model = models.Sequential([
            base_model,
            layers.Dense(132, activation='relu'),
            layers.Dense(64, activation='relu'),
            layers.Dense(3, activation='softmax')
        ])
        
        # Compile with same optimizer as training
        adam = Adam(learning_rate=0.001)
        model.compile(
            loss='categorical_crossentropy',
            optimizer=adam,
            metrics=['accuracy']
        )
        
        return model
    
    def predict(self, image_path):
        """
        Predict the animal in the image using the custom trained model
        
        Args:
            image_path: Path to the image file
            
        Returns:
            tuple: (animal_type, confidence_score)
                   animal_type: 'dog', 'cat', or 'bird'
                   confidence_score: float between 0 and 1
        """
        try:
            # Load and preprocess image (same as training)
            img = keras_image.load_img(image_path, target_size=self.img_size)
            img_array = keras_image.img_to_array(img)
            
            # Ensure batch dimension
            if img_array.ndim == 3:
                img_array = np.expand_dims(img_array, axis=0)
            
            # Use EfficientNetB0 preprocessing
            img_array = preprocess_input(img_array)
            
            # Get predictions
            predictions = self.model.predict(img_array, verbose=0)
            
            # Get the class with highest confidence
            class_idx = int(np.argmax(predictions[0]))
            confidence = float(predictions[0][class_idx])
            animal_type = self.classes[class_idx]
            
            return animal_type, confidence
                
        except Exception as e:
            print(f"Error during prediction: {str(e)}")
            import traceback
            traceback.print_exc()
            return 'dog', 0.0


# Global model instance
_model = None


def get_classifier():
    """Get or create the global classifier instance"""
    global _model
    if _model is None:
        _model = AnimalClassifier()
    return _model


def classify_image(image_path):
    """
    Classify an image and return the result
    
    Args:
        image_path: Path to the image file
        
    Returns:
        dict: {'animal': str, 'confidence': float}
    """
    classifier = get_classifier()
    animal, confidence = classifier.predict(image_path)
    return {
        'animal': str(animal),
        'confidence': float(confidence)
    }
