"""
Django settings for config project.
"""

from pathlib import Path
import os
import dj_database_url  # ✅ تأكد إنه موجود في requirements.txt

BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ مفتاح سري (من Railway أو Render)
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key")

# ✅ وضع التصحيح (من Railway/Render)
DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"

# ✅ السماح لجميع الهوستات أو تحديد الدومين لاحقًا
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")

# ✅ أضف دومين Railway الخاص بك هنا لتفادي خطأ CSRF
CSRF_TRUSTED_ORIGINS = [
    "https://web-production-3d9d6.up.railway.app",  # عدّل هذا لدومين مشروعك Railway
]

# ✅ التطبيقات
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'courses',
    'students',
    'videos',
    'cloudinary',
    'cloudinary_storage',  # ✅ لأجل رفع الفيديوهات والصور على Cloudinary
]

AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ لملفات static
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ✅ قاعدة البيانات (PostgreSQL من Railway أو SQLite محليًا)
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
        ssl_require=False
    )
}

# ✅ تحقق كلمات المرور
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ✅ اللغة والمنطقة
LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Asia/Riyadh'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOGIN_REDIRECT_URL = '/'
LOCALE_PATHS = [BASE_DIR / 'locale']

# ✅ الملفات الثابتة
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ✅ الملفات المرفوعة عبر Cloudinary
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ✅ أحجام الملفات
DATA_UPLOAD_MAX_MEMORY_SIZE = 209715200  # 200 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 209715200

# ✅ تعطيل DEBUG تلقائيًا عند النشر
if os.environ.get('RAILWAY_ENVIRONMENT_NAME'):  # Railway يرسل هذا المتغير تلقائي
    DEBUG = False
