import json
import traceback
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from datetime import timedelta

from .models import Classification, UserProfile, TwoFactorToken
from .forms import ImageUploadForm, UserRegistrationForm, UserLoginForm, TwoFactorVerificationForm

# Try to import the ML model, but handle gracefully if TensorFlow isn't installed
try:
    from .ml_model import classify_image
    ML_AVAILABLE = True
except ImportError as e:
    ML_AVAILABLE = False
    ML_ERROR = str(e)


def send_2fa_email(user, purpose='login'):
    """Send 2FA code to user email"""
    # Generate 6-digit code
    token_code = str(random.randint(100000, 999999))
    
    # Create token
    expires_at = timezone.now() + timedelta(
        minutes=settings.TWO_FA_TOKEN_EXPIRY_MINUTES
    )
    
    two_fa_token = TwoFactorToken.objects.create(
        user=user,
        token=token_code,
        purpose=purpose,
        expires_at=expires_at
    )
    
    # Send email
    subject = f'Your 2FA Code - Animal Classifier'
    message = f'''
Hello {user.first_name or user.username},

Your 2FA verification code is: {token_code}

This code will expire in {settings.TWO_FA_TOKEN_EXPIRY_MINUTES} minutes.

If you didn't request this code, please ignore this email.

Best regards,
Animal Classifier Team
    '''
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return True, token_code  # Return code for testing
    except Exception as e:
        print(f"Error sending 2FA email: {e}")
        return False, None


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('classifier:index')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.get_or_create(user=user)
            
            # Send 2FA code for signup verification
            success, code = send_2fa_email(user, purpose='signup')
            if not success:
                return render(request, 'classifier/register.html', {
                    'form': form,
                    'error': 'Failed to send verification email. Please try again.'
                })
            
            # Store user ID in session for 2FA verification
            request.session['temp_user_id'] = user.id
            return redirect('classifier:verify_signup_2fa')
        else:
            return render(request, 'classifier/register.html', {'form': form})
    else:
        form = UserRegistrationForm()
    
    return render(request, 'classifier/register.html', {'form': form})


def verify_signup_2fa(request):
    """Verify 2FA code during signup"""
    user_id = request.session.get('temp_user_id')
    if not user_id:
        return redirect('classifier:register')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = TwoFactorVerificationForm(request.POST)
        if form.is_valid():
            token_code = form.cleaned_data['token']
            
            # Verify token
            try:
                token = TwoFactorToken.objects.get(
                    user=user,
                    token=token_code,
                    purpose='signup'
                )
                
                if not token.is_valid():
                    return render(request, 'classifier/verify_2fa.html', {
                        'form': form,
                        'error': 'Code has expired. Please request a new one.',
                        'is_signup': True
                    })
                
                # Mark token as used
                token.is_used = True
                token.save()
                
                # Update profile
                profile = user.profile
                profile.two_fa_verified = True
                profile.save()
                
                # Log user in
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                del request.session['temp_user_id']
                
                return redirect('classifier:index')
            except TwoFactorToken.DoesNotExist:
                return render(request, 'classifier/verify_2fa.html', {
                    'form': form,
                    'error': 'Invalid verification code. Please try again.',
                    'is_signup': True
                })
    else:
        form = TwoFactorVerificationForm()
    
    return render(request, 'classifier/verify_2fa.html', {
        'form': form,
        'is_signup': True,
        'email': user.email
    })


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('classifier:index')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Try to authenticate with username
            user = authenticate(request, username=username, password=password)
            
            # If not found, try with email
            if not user:
                try:
                    user_by_email = User.objects.get(email=username)
                    user = authenticate(request, username=user_by_email.username, password=password)
                except User.DoesNotExist:
                    user = None
            
            if user is not None:
                # Send 2FA code
                success, code = send_2fa_email(user, purpose='login')
                if not success:
                    return render(request, 'classifier/login.html', {
                        'form': form,
                        'error': 'Failed to send verification email. Please try again.'
                    })
                
                # Store user ID and password in session for 2FA verification
                request.session['temp_user_id'] = user.id
                return redirect('classifier:verify_login_2fa')
            else:
                return render(request, 'classifier/login.html', {
                    'form': form,
                    'error': 'Invalid username/email or password.'
                })
    else:
        form = UserLoginForm()
    
    return render(request, 'classifier/login.html', {'form': form})


def verify_login_2fa(request):
    """Verify 2FA code during login"""
    user_id = request.session.get('temp_user_id')
    if not user_id:
        return redirect('classifier:login')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = TwoFactorVerificationForm(request.POST)
        if form.is_valid():
            token_code = form.cleaned_data['token']
            
            try:
                token = TwoFactorToken.objects.get(
                    user=user,
                    token=token_code,
                    purpose='login'
                )
                
                if not token.is_valid():
                    return render(request, 'classifier/verify_2fa.html', {
                        'form': form,
                        'error': 'Code has expired. Please request a new one.',
                        'is_signup': False
                    })
                
                # Mark token as used
                token.is_used = True
                token.save()
                
                # Log user in
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                del request.session['temp_user_id']
                
                return redirect('classifier:index')
            except TwoFactorToken.DoesNotExist:
                return render(request, 'classifier/verify_2fa.html', {
                    'form': form,
                    'error': 'Invalid verification code. Please try again.',
                    'is_signup': False
                })
    else:
        form = TwoFactorVerificationForm()
    
    return render(request, 'classifier/verify_2fa.html', {
        'form': form,
        'is_signup': False,
        'email': user.email
    })


def logout_view(request):
    """User logout view"""
    logout(request)
    return redirect('classifier:login')


@login_required(login_url='classifier:login')
def index(request):
    """Render the main page with upload interface"""
    form = ImageUploadForm()
    return render(request, 'classifier/index.html', {'form': form})


@require_http_methods(["POST"])
@login_required(login_url='classifier:login')
def upload_image(request):
    """Handle image upload and classification"""
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        
        if form.is_valid() and 'image' in request.FILES:
            try:
                # Check if ML model is available
                if not ML_AVAILABLE:
                    return JsonResponse({
                        'success': False,
                        'error': f'ML model not available. TensorFlow may not be installed. Error: {ML_ERROR}'
                    }, status=503)
                
                # Save the image first without committing
                classification = form.save(commit=False)
                classification.user = request.user  # Assign to logged-in user
                
                # Set default values to avoid NULL constraint
                classification.prediction = 'dog'  # Default value
                classification.confidence = 0.0    # Default value
                classification.save()
                
                # Get the full path of the saved image
                image_path = classification.image.path
                
                # Perform classification
                result = classify_image(image_path)
                
                # Update the classification with actual results
                classification.prediction = result['animal']
                classification.confidence = result['confidence']
                classification.save()
                
                return JsonResponse({
                    'success': True,
                    'prediction': classification.prediction,
                    'confidence': f"{classification.confidence:.2%}",
                    'image_url': classification.image.url,
                    'id': classification.id,
                })
            except Exception as e:
                # Log the full error for debugging
                error_msg = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
                print(f"Classification error: {error_msg}")
                
                return JsonResponse({
                    'success': False,
                    'error': f'Classification failed: {str(e)}'
                }, status=500)
        else:
            return JsonResponse({
                'success': False,
                'error': 'Invalid form or no image provided'
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'error': 'Only POST requests are allowed'
    }, status=405)


@login_required(login_url='classifier:login')
def history(request):
    """Display classification history - only user's own predictions"""
    # Only show classifications for the logged-in user
    classifications = Classification.objects.filter(user=request.user)[:20]
    return render(request, 'classifier/history.html', {
        'classifications': classifications
    })


@login_required(login_url='classifier:login')
def statistics(request):
    """Display user statistics dashboard"""
    # Get all user's classifications
    classifications = Classification.objects.filter(user=request.user)
    
    # Calculate statistics
    total_predictions = classifications.count()
    
    # Count by animal type
    dog_count = classifications.filter(prediction='dog').count()
    cat_count = classifications.filter(prediction='cat').count()
    bird_count = classifications.filter(prediction='bird').count()
    
    # Calculate average confidence
    if total_predictions > 0:
        avg_confidence = sum(
            [c.confidence for c in classifications]
        ) / total_predictions
    else:
        avg_confidence = 0
    
    # Get highest confidence prediction
    highest_confidence = classifications.order_by('-confidence').first()
    
    # Get most common prediction
    from django.db.models import Count
    most_common = classifications.values('prediction').annotate(
        count=Count('prediction')
    ).order_by('-count').first()
    
    # Recent predictions (last 7 days)
    from datetime import timedelta
    from django.utils import timezone
    last_7_days = timezone.now() - timedelta(days=7)
    recent_count = classifications.filter(created_at__gte=last_7_days).count()
    
    # Confidence distribution
    high_confidence = classifications.filter(confidence__gte=0.8).count()
    medium_confidence = classifications.filter(confidence__gte=0.6, confidence__lt=0.8).count()
    low_confidence = classifications.filter(confidence__lt=0.6).count()
    
    stats = {
        'total_predictions': total_predictions,
        'dog_count': dog_count,
        'cat_count': cat_count,
        'bird_count': bird_count,
        'dog_percentage': (dog_count / total_predictions * 100) if total_predictions > 0 else 0,
        'cat_percentage': (cat_count / total_predictions * 100) if total_predictions > 0 else 0,
        'bird_percentage': (bird_count / total_predictions * 100) if total_predictions > 0 else 0,
        'avg_confidence': f"{avg_confidence:.2%}",
        'highest_confidence': highest_confidence,
        'most_common': most_common['prediction'] if most_common else 'N/A',
        'recent_predictions_7days': recent_count,
        'high_confidence_count': high_confidence,
        'medium_confidence_count': medium_confidence,
        'low_confidence_count': low_confidence,
    }
    
    return render(request, 'classifier/statistics.html', {
        'stats': stats
    })

