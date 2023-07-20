import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.scrubber import EventScrubber

from . import allowed_domains
from .settings_base import (
    BASE_DIR,
    SECRET_KEY,
    STATIC_ROOT,
    STATIC_URL,
    STATICFILES_DIRS,
    env,
)

SECRET_KEY = SECRET_KEY
STATIC_URL = STATIC_URL
STATICFILES_DIRS = STATICFILES_DIRS
STATIC_ROOT = STATIC_ROOT

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

CONTACT_EMAIL = env.str("CONTACT_EMAIL", default="test@example.com")
FROM_EMAIL = env.str("FROM_EMAIL", default="test@example.com")
FEEDBACK_EMAIL = env.str("FEEDBACK_EMAIL", default="test@example.com")

VCAP_APPLICATION = env.json("VCAP_APPLICATION", default={})

BASE_URL = env.str("BASE_URL")
BASIC_AUTH = env.str("BASIC_AUTH", default="")

APPEND_SLASH = True

ALLOWED_HOSTS = [
    "etf-develop.london.cloudapps.digital",
    "etf-sandbox.london.cloudapps.digital",
    "etf-staging.london.cloudapps.digital",
    "etf-testing.london.cloudapps.digital",
    "evaluation-registry.service.gov.uk",
    "etf.london.cloudapps.digital",
    "localhost",
    "127.0.0.1",
    "eva-reg-testserver",
]

HOST_MAP = {
    "http://localhost:8010/": "http://127.0.0.1:8010",
    "https://etf-develop.london.cloudapps.digital": "https://etf-develop.london.cloudapps.digital",
    "https://etf-staging.london.cloudapps.digital": "https://etf-staging.london.cloudapps.digital",
}

if DEBUG:
    CORS_ALLOWED_ORIGINS = [HOST_MAP[BASE_URL]]


# Application definition

INSTALLED_APPS = [
    "eva_reg.evaluation",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
]

CORS_APPS = [
    "corsheaders",
]

if DEBUG:
    INSTALLED_APPS = INSTALLED_APPS + CORS_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "eva_reg.evaluation.session_middleware.MaxAgeSessionMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "global_login_required.GlobalLoginRequiredMiddleware",
]

if BASIC_AUTH:
    MIDDLEWARE = ["eva_reg.auth.basic_auth_middleware"] + MIDDLEWARE

if VCAP_APPLICATION.get("space_name", "unknown") not in ["tests", "local"]:
    SESSION_COOKIE_SECURE = True

SESSION_COOKIE_AGE = env.int("SESSION_COOKIE_AGE", default=60 * 60 * 24)  # Rolling timeout of 24 hours
SESSION_MAX_AGE = env.int("SESSION_MAX_AGE", default=60 * 60 * 24 * 7)  # Forced logout 7 days after login
SESSION_SAVE_EVERY_REQUEST = True

# CSRF settings
CSRF_COOKIE_HTTPONLY = True

CORS_MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
]

if DEBUG:
    MIDDLEWARE = MIDDLEWARE + CORS_MIDDLEWARE

ROOT_URLCONF = "eva_reg.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [
            BASE_DIR / "eva_reg" / "templates",
        ],
        "OPTIONS": {
            "environment": "eva_reg.jinja2.environment",
        },
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "eva_reg" / "templates" / "allauth",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "eva_reg.evaluation.context_processors.space_name",
            ],
        },
    },
]

WSGI_APPLICATION = "eva_reg.wsgi.application"

DATABASES = {
    "default": {
        **env.db("DATABASE_URL"),
        **{"ATOMIC_REQUESTS": True},
    }
}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SENTRY_DSN = env.str("SENTRY_DSN", default="")
SENTRY_ENVIRONMENT = env.str("SENTRY_ENVIRONMENT", default="")

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[
        DjangoIntegration(),
    ],
    environment=SENTRY_ENVIRONMENT,
    event_scrubber=EventScrubber(),  # this is set by default
    send_default_pii=False,
    traces_sample_rate=0.0,
)

AUTH_USER_MODEL = "evaluation.User"

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
SITE_ID = 1
LOGIN_REDIRECT_URL = "index"

ALLOW_EXAMPLE_EMAILS = env.bool("ALLOW_EXAMPLE_EMAILS", default=True)


if ALLOW_EXAMPLE_EMAILS:
    ALLOWED_CIVIL_SERVICE_DOMAINS = allowed_domains.CIVIL_SERVICE_DOMAINS.union({"example.com"})
    # This is domain is used for testing, so for these purposes, count it as a CS domain
else:
    ALLOWED_CIVIL_SERVICE_DOMAINS = allowed_domains.CIVIL_SERVICE_DOMAINS

PASSWORD_RESET_TIMEOUT = 60 * 60 * 24

SEND_VERIFICATION_EMAIL = env.bool("SEND_VERIFICATION_EMAIL", default=False)

# Email

EMAIL_BACKEND_TYPE = env.str("EMAIL_BACKEND_TYPE")

if EMAIL_BACKEND_TYPE == "FILE":
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = env.str("EMAIL_FILE_PATH")
elif EMAIL_BACKEND_TYPE == "CONSOLE":
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
elif EMAIL_BACKEND_TYPE == "GOVUKNOTIFY":
    EMAIL_BACKEND = "django_gov_notify.backends.NotifyEmailBackend"
    GOVUK_NOTIFY_API_KEY = env.str("GOVUK_NOTIFY_API_KEY")
    GOVUK_NOTIFY_PLAIN_EMAIL_TEMPLATE_ID = env.str("GOVUK_NOTIFY_PLAIN_EMAIL_TEMPLATE_ID")
else:
    if EMAIL_BACKEND_TYPE not in ("FILE", "CONSOLE", "GOVUKNOTIFY"):
        raise Exception(f"Unknown EMAIL_BACKEND_TYPE of {EMAIL_BACKEND_TYPE}")

SEND_VERIFICATION_EMAIL = env.bool("SEND_VERIFICATION_EMAIL", default=False)

if DEBUG:
    ACCOUNT_RATE_LIMITS = {}


PUBLIC_PATHS = [
    "",
    "accounts/signup/",
    "accounts/login/",
    "accounts/password-reset/",
    "accounts/change-password/reset/",
]
