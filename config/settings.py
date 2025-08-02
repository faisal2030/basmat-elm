"""
Django settings for config project.
"""

from pathlib import Path
import os
import dj_database_url  # ✅ تأكد إنه موجود في requirements.txt

BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ مفتاح سري (من Render)
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key")

# ✅ وضع التصحيح (من Render)
DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"

# ✅ السماح لجميع الهوستات أو تحديد الدومين لاحقًا
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")

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
]

AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ ملفات ثابتة
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
                # ✅ احذف السطر التالي إذا ما عندك context_processors.site_name
                # 'config.context_processors.site_name',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ✅ قاعدة البيانات (PostgreSQL على Render أو SQLite محليًا)
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

# ✅ Whitenoise لضغط الملفات
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ✅ الملفات المرفوعة
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ✅ أحجام الملفات
DATA_UPLOAD_MAX_MEMORY_SIZE = 209715200  # 200 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 209715200

# ✅ تعطيل DEBUG تلقائيًا إذا كنا على Render
if os.environ.get('RENDER'):
    DEBUG = False
