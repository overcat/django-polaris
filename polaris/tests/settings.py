from settings import *
from polaris import settings

STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
settings.LOCAL_MODE = False
SESSION_COOKIE_SECURE = True
INSTALLED_APPS.remove("server")
ROOT_URLCONF = "polaris.urls"
