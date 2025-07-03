from django.contrib import admin
from .models import Subject, Chapter, Topic,Question, ModelTestAttempt

# Register your models here.
admin.site.register(Subject)
admin.site.register(Chapter)
admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(ModelTestAttempt)





