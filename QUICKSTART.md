# 🐾 Animal Classifier - Quick Start Guide

## ⚡ Quick Setup (2 minutes)

### Step 1: Install Dependencies
```bash
cd /home/el_pepe/Documents/animalerie
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Setup Database
```bash
python manage.py migrate
```

### Step 3: Run Server
```bash
python manage.py runserver
```

### Step 4: Open Browser
Visit: **http://localhost:8000**

---

## 📝 Key Features

✅ **Drag & Drop Upload** - Just drag an image to upload  
✅ **Instant Classification** - AI classifies: Dog, Cat, or Bird  
✅ **Confidence Score** - Shows how certain the prediction is  
✅ **History Tracking** - View all classifications  
✅ **Admin Dashboard** - Manage classifications at `/admin`  

---

## 📁 Project Files

| File | Purpose |
|------|---------|
| `classifier/views.py` | Handles requests and AI predictions |
| `classifier/models.py` | Database structure for classifications |
| `classifier/ml_model.py` | AI model logic using TensorFlow |
| `classifier/templates/` | HTML pages for the app |
| `malla/settings.py` | Django configuration |
| `malla/urls.py` | URL routing |

---

## 🎯 How to Use

1. **Upload Image**
   - Click the upload box or drag an image
   - Wait for processing (usually 2-3 seconds)

2. **View Result**
   - See if it's a Dog, Cat, or Bird
   - Check confidence percentage

3. **View History**
   - Click "View Classification History"
   - See all past classifications

---

## 🔧 Useful Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run development server
python manage.py runserver

# Run with specific port
python manage.py runserver 8080

# Access admin panel
# URL: http://localhost:8000/admin

# Create superuser
python manage.py createsuperuser

# Stop server
Ctrl + C
```

---

## 🚨 Troubleshooting

**Problem**: TensorFlow installation fails
```bash
pip install tensorflow --upgrade
```

**Problem**: Port 8000 already in use
```bash
python manage.py runserver 8080
```

**Problem**: Database errors
```bash
python manage.py migrate
```

---

## 🎓 How It Works

1. **You upload an image** ↓
2. **Django saves it** ↓
3. **TensorFlow analyzes it** ↓
4. **AI detects: Dog/Cat/Bird** ↓
5. **Result stored in database** ↓
6. **You see the answer!** ✨

---

## 📊 Project Structure

```
animalerie/
├── classifier/          ← Main app files
│   ├── views.py        ← View functions
│   ├── models.py       ← Database models
│   ├── ml_model.py     ← AI classification
│   └── templates/      ← HTML pages
├── malla/              ← Django project config
├── media/              ← Uploaded images
├── manage.py           ← Django commands
├── requirements.txt    ← Dependencies
└── README.md           ← Full documentation
```

---

## 🌐 URLs

| URL | Purpose |
|-----|---------|
| `http://localhost:8000/` | Main classifier page |
| `http://localhost:8000/history/` | View classification history |
| `http://localhost:8000/admin/` | Admin panel |

---

## 💡 Tips

- First upload takes longer (model loading) ~10-15 seconds
- Subsequent uploads are faster ~2-3 seconds
- Works with JPG, PNG, GIF, and more
- Best results with clear animal images

---

## 🚀 Next Steps

1. **Test the app** - Upload some animal images
2. **Check admin** - Go to `/admin` to see saved classifications
3. **Explore code** - Check `ml_model.py` to understand AI logic
4. **Customize** - Modify templates to change appearance
5. **Deploy** - Use Gunicorn for production

---

For detailed information, see **README.md**
