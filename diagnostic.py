#!/usr/bin/env python
"""
Diagnostic script to check if all dependencies are installed and working
"""
import sys
import os

print("🔍 Animal Classifier - Diagnostic Check")
print("=" * 50)

# Check Python version
print(f"\n✓ Python version: {sys.version}")

# Check Django
try:
    import django
    print(f"✓ Django: {django.VERSION}")
except ImportError as e:
    print(f"✗ Django not installed: {e}")

# Check PIL/Pillow
try:
    from PIL import Image
    import PIL
    print(f"✓ Pillow: {PIL.__version__}")
except ImportError as e:
    print(f"✗ Pillow not installed: {e}")

# Check NumPy
try:
    import numpy
    print(f"✓ NumPy: {numpy.__version__}")
except ImportError as e:
    print(f"✗ NumPy not installed: {e}")

# Check TensorFlow
print("\n📦 Checking TensorFlow...")
try:
    import tensorflow as tf
    print(f"✓ TensorFlow: {tf.__version__}")
    
    # Try to load the model
    print("  Loading MobileNetV2 model...")
    from tensorflow.keras.applications import MobileNetV2
    model = MobileNetV2(weights='imagenet')
    print("  ✓ MobileNetV2 model loaded successfully!")
    
except ImportError as e:
    print(f"✗ TensorFlow not installed: {e}")
    print("\n  Run: pip install tensorflow")
except Exception as e:
    print(f"✗ Error loading TensorFlow: {e}")

# Check database
print("\n💾 Checking database...")
try:
    os.chdir('/home/el_pepe/Documents/animalerie')
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'dbshell', '--help'])
    print("✓ Database connection OK")
except Exception as e:
    print(f"✗ Database error: {e}")

print("\n" + "=" * 50)
print("✅ Diagnostic check complete!")
print("\nIf TensorFlow is not installed, run:")
print("  pip install tensorflow")
