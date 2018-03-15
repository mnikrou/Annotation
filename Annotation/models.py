
from django.db import models
from django.contrib.auth.models import User
import datetime 

class Image(models.Model):
    img = models.ImageField(upload_to = 'photos/', default = 'photos/None/no-img.jpg')
    order = models.IntegerField(null=True, blank=True)

    def delete(self, *args, **kwargs):
        storage, path = self.img.storage, self.img.path
        super(Image, self).delete(*args, **kwargs)
        storage.delete(path)

    class Meta:
        db_table = 'Images'

class ImageAnnotation(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    image = models.ForeignKey(Image, on_delete=models.PROTECT)
    annotation_json = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True) 

    class Meta:
        db_table = 'ImageAnnotations'
