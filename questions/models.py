from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
import pytz 

User = get_user_model()

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=200)
    
    
    def __str__(self):
        return self.name

class Chapter(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    chapter_number = models.CharField(max_length=10)  # Format like "1.1", "1.2"
    name = models.CharField(max_length=200)
      # Comma-separated list of topics  
    
    class Meta:
        unique_together = ['subject', 'chapter_number']
        ordering = ['subject', 'chapter_number']
    
    def __str__(self):
        return f"{self.chapter_number} - {self.name}"


class Topic(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="topics")
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.chapter} - {self.name}"

class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium')
    ]

    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100)
    question = models.TextField()
    options = models.JSONField()
    answer = models.CharField(max_length=1)  # Stores 'A', 'B', 'C', etc.
    explanation = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    
    class Meta:
        ordering = ['chapter', 'difficulty']
    
    def __str__(self):
        return f"{self.question[:50]}..."

    def get_correct_answer(self):
        index = ord(self.answer.upper()) - ord('A')
        return self.options[index] if 0 <= index < len(self.options) else None
    

class ModelTestAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    correct = models.PositiveIntegerField()
    wrong = models.PositiveIntegerField()
    unattempted = models.PositiveIntegerField()
    score = models.FloatField()

    def __str__(self):
         # Handle possible None value for timestamp
        if self.timestamp:
            # Convert UTC time to Nepal time
            kathmandu_tz = pytz.timezone('Asia/Kathmandu')
            local_time = timezone.localtime(self.timestamp, timezone=kathmandu_tz)
            return f"{self.user} - {local_time.strftime('%Y-%m-%d %H:%M')} (NPT)"
        return f"{self.user} - [No timestamp]"

    class Meta:
        ordering = ['-timestamp']