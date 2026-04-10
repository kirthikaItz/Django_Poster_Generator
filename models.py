from django.db import models

class EventPoster(models.Model):
    title = models.CharField(max_length=200)
    resource_person = models.CharField(max_length=100)
    event_date = models.DateField()
    coordinator_name = models.CharField(max_length=100)
    recipient_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.event_date}"