"""
Utility script for making predictions with the Animal Classifier model
Usage: python predict.py <image_path>
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from classifier.ml_model import classify_image


def predict_single_image(image_path):
    """
    Make a prediction on a single image
    
    Args:
        image_path: Path to the image file
    """
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return
    
    print(f"\nClassifying image: {image_path}")
    print("-" * 50)
    
    try:
        result = classify_image(image_path)
        
        animal = result['animal']
        confidence = result['confidence']
        
        print(f"Animal Type: {animal.upper()}")
        print(f"Confidence: {confidence:.2%}")
        print("-" * 50)
        
        return result
        
    except Exception as e:
        print(f"Error during prediction: {e}")
        import traceback
        traceback.print_exc()


def predict_batch(image_folder):
    """
    Make predictions on all images in a folder
    
    Args:
        image_folder: Path to folder containing images
    """
    if not os.path.isdir(image_folder):
        print(f"Error: Folder not found at {image_folder}")
        return
    
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
    image_files = [f for f in os.listdir(image_folder) 
                   if os.path.splitext(f)[1].lower() in image_extensions]
    
    if not image_files:
        print(f"No images found in {image_folder}")
        return
    
    print(f"\nFound {len(image_files)} images in {image_folder}")
    print("=" * 60)
    
    results = []
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        try:
            result = classify_image(image_path)
            results.append({
                'filename': image_file,
                'animal': result['animal'],
                'confidence': result['confidence']
            })
            
            print(f"{image_file:30} → {result['animal']:6} ({result['confidence']:.2%})")
            
        except Exception as e:
            print(f"{image_file:30} → ERROR: {str(e)[:30]}")
            results.append({
                'filename': image_file,
                'animal': 'ERROR',
                'confidence': 0.0
            })
    
    print("=" * 60)
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Single image:  python predict.py <image_path>")
        print("  Batch images:  python predict.py <folder_path>")
        print("\nExample:")
        print("  python predict.py /path/to/dog.jpg")
        print("  python predict.py /path/to/images_folder/")
        sys.exit(1)
    
    path = sys.argv[1]
    
    if os.path.isfile(path):
        # Single image
        predict_single_image(path)
    elif os.path.isdir(path):
        # Batch of images
        predict_batch(path)
    else:
        print(f"Error: Path does not exist: {path}")
        sys.exit(1)
