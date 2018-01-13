from django.db import models
import datetime

class Todo(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    deadline = models.DateTimeField(default=(datetime.datetime.now() + datetime.timedelta(days=1)), blank=True)
    def __str__(self):
        return self.title


