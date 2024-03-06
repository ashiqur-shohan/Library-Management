from django.db import models
from category.models import CategoryModel
from django.contrib.auth.models import User
# Create your models here.


class BookModel(models.Model):
    image = image = models.ImageField(
        upload_to='book/media/uploads', blank=True, null=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    desc = models.TextField()
    category = models.ManyToManyField(CategoryModel)

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(
        BookModel, on_delete=models.CASCADE, related_name='review')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
