from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Ensure this matches your app name (poster_app) 
# and the function name in your views.py
from poster_app.views import generate_and_send_poster 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', generate_and_send_poster, name='generate_poster'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)