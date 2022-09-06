from django import template
from django.db.models import Q,Count
from datetime import datetime, timedelta
from category.models import Category
from blog.models import BlogModel


register = template.Library()
@register.inclusion_tag('partials/_tag_navbar.html')
def navbar(request):
	user=request.user
	categories=Category.objects.filter(active=True)
	return {'categories':categories,'request':request,'user':user}



@register.inclusion_tag('partials/_trend_articles.html')
def popular_articles():
	last_month=datetime.today()-timedelta(days=30)
	articles=BlogModel.objects.annotate(counter=Count('hit',filter=Q(hitdate__created__gt=last_month))).filter(is_publish='p')

	return {'articles':articles}



@register.inclusion_tag('partials/_delete_modal.html')
def delete_modal(article):
	article=article
	return {'article':article}