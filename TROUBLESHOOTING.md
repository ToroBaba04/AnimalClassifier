# 🐾 Troubleshooting Guide

## Problem: "Error uploading image: Unexpected token '<', <!DOCTYPE..." 

This error means the server returned HTML instead of JSON, usually indicating a server-side error.

### Solutions:

#### 1. **Database Not Set Up**
```bash
python manage.py migrate
```

#### 2. **TensorFlow Not Installed**
```bash
pip install tensorflow
```

#### 3. **CSRF Token Issue**
Make sure you've made a GET request to the page first (to set the CSRF cookie) before uploading.
- Refresh the page: `Ctrl+F5` (hard refresh)
- Try again

#### 4. **Check Django Logs**
Look at the terminal where you ran `runserver`. The error traceback will be printed there.

#### 5. **Missing Migrations**
```bash
python manage.py makemigrations classifier
python manage.py migrate
```

---

## Problem: "Forbidden (CSRF cookie not set)"

### Solution:
- Make sure you've loaded the page in your browser first
- Hard refresh: `Ctrl+F5` (or `Cmd+Shift+R` on Mac)
- The CSRF token is set when you load the page

---

## Problem: "no such table: classifier_classification"

### Solution:
```bash
python manage.py migrate
```

---

## Problem: Drag and drop not working

### Solution:
- Use a modern browser (Chrome, Firefox, Safari, Edge)
- Make sure JavaScript is enabled
- Try the "Choose Image" button instead
- Check browser console for errors: `F12` → Console tab

---

## Complete Setup From Scratch

If you want to start fresh:

```bash
# 1. Stop the server (Ctrl+C in terminal)

# 2. Remove old database
rm db.sqlite3

# 3. Create fresh migrations
python manage.py makemigrations classifier

# 4. Migrate
python manage.py migrate

# 5. Create superuser (optional)
python manage.py createsuperuser

# 6. Run server
python manage.py runserver

# 7. Visit http://localhost:8000
```

---

## Check TensorFlow Installation

```bash
python -c "import tensorflow; print(tensorflow.__version__)"
```

If this fails, run:
```bash
pip install tensorflow
```

---

## Debug Mode

To see detailed error messages:

1. Add this to `malla/settings.py`:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

2. Restart the server to see detailed logs

---

## Network/Firewall Issues

If you get connection errors:

1. Try different port:
```bash
python manage.py runserver 8080
```

2. Visit: `http://localhost:8080`

---

## Browser Console Errors

Press `F12` to open Developer Tools:
- Check the "Console" tab for JavaScript errors
- Check the "Network" tab to see the request/response
- Look for the upload request and click it to see the response

---

## Still Having Issues?

Check these files in order:
1. Terminal output from `runserver` - look for error messages
2. [classifier/ml_model.py](classifier/ml_model.py) - AI model code
3. [classifier/views.py](classifier/views.py) - Upload handler code
4. [classifier/templates/classifier/index.html](classifier/templates/classifier/index.html) - Frontend code

The error message in the terminal will tell you exactly what went wrong!
