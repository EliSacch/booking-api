from django.db import models
from django.contrib.postgres.fields import ArrayField


class Service(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=20.00)
    duration = models.IntegerField()
    image = models.ImageField(
        upload_to='images/', default='../default-service_obfy3s'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title}"