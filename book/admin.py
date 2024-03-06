from django.contrib import admin
from .models import BookModel,Review
# Register your models here.

admin.site.register(BookModel)
admin.site.register(Review)