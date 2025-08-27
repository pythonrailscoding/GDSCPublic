from django.contrib.auth.models import User
from django.db import models
from .validators import file_limit, validate_image_extension
from ckeditor.fields import RichTextField

import os

from django_resized import ResizedImageField

class CategoryModel(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return " "

class TagsModel(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return " "

class BlogModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = RichTextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    thumbnail = ResizedImageField(size=[232, 216] ,quality=90 ,upload_to="thumbnails/%y", validators=[validate_image_extension, file_limit], default=None)

    # Categories and Tags
    category = models.ManyToManyField(CategoryModel, related_name="category")
    tags = models.ManyToManyField(TagsModel, related_name="tags")

    def __str__(self):
        return str(self.user) + " has made a blog about " + str(self.title)[:20] + "..... "

    def save(self, *args, **kwargs):
        try:
            # If updating, check old photo
            old_profile = BlogModel.objects.get(id=self.id)
            if old_profile.thumbnail and old_profile.thumbnail != self.thumbnail:
                old_path = old_profile.thumbnail.path
                if os.path.isfile(old_path):
                    os.remove(old_path)  # delete old photo
        except BlogModel.DoesNotExist:
            pass  # first time creating profile, so no old photo

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # When deleting profile, also delete photo
        if self.thumbnail and os.path.isfile(self.thumbnail.path):
            os.remove(self.thumbnail.path)
        super().delete(*args, **kwargs)

class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(BlogModel, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.user)  + " has made a comment about " + str(self.blog)[:20] + "..... "

    class Meta:
        ordering = ['-id']

