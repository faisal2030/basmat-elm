"""
Django settings for config project.
"""

from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ====== الأساسيات ======
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key")
DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"

# السماح بالمضيفين (يمكن تمرير قائمة مفصولة بفواصل من المتغير)
ALLOWED_HOSTS = [
    "basmat-elm.up.railway.app"
]

CSRF_TRUSTED_ORIGINS = [
    "https://basmat-elm.up.railway.app"
]

# CSRF Trusted Origins — نحاول قراءته تلقائيًا من Railway
CSRF_TRUSTED_ORIGINS = []
RAILWAY_DOMAIN = os.environ.get("RAILWAY_PUBLIC_DOMAIN")
if RAILWAY_DOMAIN:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RAILWAY_DOMAIN}")

# لو عندك نطاق ثابت آخر، أضِفه هنا يدويًا (اختياري):
# CSRF_TRUSTED_ORIGINS += ["https://your-custom-domain.com"]

# ====== التطبيقات ======
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "accounts",
    "courses",
    "students",
    "videos",

    # تخزين الوسائط على Cloudinary
    "cloudinary",
    "cloudinary_storage",
]

AUTH_USER_MODEL = "accounts.User"

# ====== الميدلوير ======
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # لملفات static
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# ====== القوالب ======
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ====== قاعدة البيانات (Postgres من Railway أو SQLite محليًا) ======
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
        ssl_require=False,  # اجعلها True إذا كانت قاعدة Railway تتطلب SSL
    )
}

# ====== تحقق كلمات المرور ======
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ====== اللغة والمنطقة ======
LANGUAGE_CODE = "ar"
TIME_ZONE = "Asia/Riyadh"
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOGIN_REDIRECT_URL = "/"
LOCALE_PATHS = [BASE_DIR / "locale"]

# ====== الملفات الثابتة (Static) ======
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ====== الملفات المرفوعة (Media) عبر Cloudinary ======
# يعتمد على متغير البيئة CLOUDINARY_URL بصيغة:
# CLOUDINARY_URL=cloudinary://<API_KEY>:<API_SECRET>@<CLOUD_NAME>
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # لن تُستخدم فعليًا مع Cloudinary، لا ضرر من وجودها

# ====== أحجام الرفع ======
DATA_UPLOAD_MAX_MEMORY_SIZE = 209715200  # 200 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 209715200

# ====== إعدادات أمان إضافية في الإنتاج ======
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
