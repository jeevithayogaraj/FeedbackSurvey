from django.db import models
from django.utils import timezone

# Create your models here.
class Review (models.Model):
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    review = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)    
    def __str__(self):
        return self.name
    
    
