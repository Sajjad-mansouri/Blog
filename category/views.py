from django.shortcuts import render
from .models import Category

def category(request,category_slug):
	category=Category.objects.get(slug=category_slug)
	articles=category.blogmodel_set.filter(is_publish=True)

	return render(request,'blog/category.html',{'articles':articles,'category':category})
