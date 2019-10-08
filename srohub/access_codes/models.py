from django.db import models

# Create your models here.


class AccessCode(models.Model):
    """An access code that can change."""

    class Meta:

        permissions = (
            ('view_access_codes', 'View Access Codes'),
            ('increment_access_codes', 'Increment Access Codes'),
        )

    name = models.CharField(max_length=30)
    counter = models.IntegerField()
    secret = models.CharField(max_length=255)

    def __str__(self):
        return self.name
