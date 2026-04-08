import os
from django.core.wsgi import get_wsgi_application
# Pas besoin d'importer WhiteNoise ici si tu l'as mis dans MIDDLEWARE (recommandé)

# Assure-toi que le nom correspond bien à ton dossier principal
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myhali_backend.settings')

application = get_wsgi_application()