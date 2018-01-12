
from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    img = models.ImageField(upload_to = 'photos/', default = 'photos/None/no-img.jpg')

    def delete(self, *args, **kwargs):
        storage, path = self.img.storage, self.img.path
        super(Image, self).delete(*args, **kwargs)
        storage.delete(path)
