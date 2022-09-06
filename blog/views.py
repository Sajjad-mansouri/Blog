from django.shortcuts import render
from django.db.models import Q
from django.http import Http404
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from .models import BlogModel,IPAddressModel
from category.models import Category

def blog(request):
	articles_all=BlogModel.objects.filter(is_publish=True)
	paginator=Paginator(articles_all,2)
	page_number = request.GET.get('page')
	articles=paginator.get_page(page_number)
	return render(request,'blog/index.html',{'articles':articles})

def search(request):
	search=request.GET.get('search')
	articles=BlogModel.objects.filter(Q(title__icontains=search)|Q(description__contains=search) and Q(is_publish='p'))
	context={'articles':articles,'search':search}
	return render(request,'blog/search.html',context)


def single(request,single_id):
	article=get_object_or_404(BlogModel,id=single_id,is_publish='p')
	
	if request.user.ip_address not in [hit.ip for hit in article.hit.all()]:
		ip=IPAddressModel.objects.get(ip=request.user.ip_address)
		hits=article.hit.add(ip)
		
		
	counter=len(article.hit.all())
	return render(request,'blog/single.html',{'article':article,'counter':counter})

def preview(request,single_id):
	article=get_object_or_404(BlogModel,id=single_id)
	if request.user.is_superuser or article.author== request.user:
		return render(request,'blog/single.html',{'article':article})
	else:
		raise Http404
