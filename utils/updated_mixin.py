
from django.db import models
from django.utils import timezone


class UpdatedCreatedMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(default=timezone.now)

    def save(self, ignore_time=False, *args, **kwargs):
        if not ignore_time:
            self.update_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
