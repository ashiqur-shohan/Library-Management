from django.shortcuts import render
from django.views.generic import TemplateView
from book.models import BookModel
from category.models import CategoryModel
# Create your views here.

# class HomeView(TemplateView):
#     template_name = 'index.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['book'] = 
#         context['title'] = 'My Django Website'
#         return context

def home(request,category_slug=None):
    data = BookModel.objects.all()
    if category_slug is not None:
        categorys = CategoryModel.objects.get(slug=category_slug)
        data = BookModel.objects.filter(category=categorys)
    categorys = CategoryModel.objects.all()
    return render(request,'index.html',{'data': data, 'category': categorys})
