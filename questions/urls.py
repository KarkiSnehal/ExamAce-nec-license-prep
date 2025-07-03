from django.contrib import admin
from django.urls import path,include

from questions import views

urlpatterns = [
    path('', views.questions, name = 'questions'),
    path('practice/chapter/<int:chapter_id>/', views.practice_chapter, name='practice_chapter'),
    path('subject/<int:subject_id>/', views.subject_view, name='subject_detail'),
    path('chapter/<int:chapter_id>/', views.chapter_view, name='chapter_detail'),
    path('model-test/', views.model_test, name='model_test'),
    path('submit-model-test/', views.submit_model_test, name='submit_model_test'),
    path('logout/', views.LogoutView, name='logout'),
   

]
