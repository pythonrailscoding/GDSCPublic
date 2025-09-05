import os
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.functional import empty

from .validators import file_limit, validate_image_extension

class VerifyMembers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user) + " " + str(self.is_verified)

class Profile(models.Model):
    user = models.ForeignKey(User, related_name="profile", on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to="profile_pic/%y", null=True, blank=True, validators=[file_limit, validate_image_extension])
    inst = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)

    def __str__(self):
        return str(self.user) + " has a bio. "

    def save(self, *args, **kwargs):
        try:
            # If updating, check old photo
            # You dont want user to upload same photo twice. That wastes space
            old_profile = Profile.objects.get(pk=self.pk)
            if old_profile.profile_pic and old_profile.profile_pic != self.profile_pic:
                old_path = old_profile.profile_pic.path
                if os.path.isfile(old_path):
                    # delete old photo
                    os.remove(old_path)
        except Profile.DoesNotExist:
            pass  # first time creating profile, so no old photo, let him do it

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # When deleting profile, also delete photo
        if self.profile_pic and os.path.isfile(self.profile_pic.path):
            os.remove(self.profile_pic.path)
        super().delete(*args, **kwargs)
