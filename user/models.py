from django.db import models


# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True, unique=True)
    password = models.CharField(max_length=200, null=True)
    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def to_dict_json(self):
        return {
            'id': self.pk,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'photo': self.photo.name,
        }

    def __str__(self):
        return self.name