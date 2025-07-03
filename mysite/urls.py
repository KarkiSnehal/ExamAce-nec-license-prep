from django.contrib import admin
from django.urls import path,include
from questions import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('startpage.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('questions/', include('questions.urls')),
    
]
