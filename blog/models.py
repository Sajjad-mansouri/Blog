from django.db import models
from account.models import User
from django.utils import timezone
from category.models import Category


class IPAddressModel(models.Model):
	ip=models.GenericIPAddressField()
	created=models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return self.ip


class BlogModel(models.Model):
	PUBLISH_CHOICES=(
('d','پیش نویس'),
('p','منتشر شده'),
('i','ارسال به مدیر'),
('b','نیاز به بررسی بیشتر')
		)
	title=models.CharField(max_length=100,verbose_name='عنوان')
	author=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,verbose_name='نویسنده')
	slug=models.SlugField(max_length=20,unique=True,verbose_name='آدرس مقاله')
	category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,verbose_name='دسته بندی')
	image=models.ImageField(upload_to='media/blog/%Y/%m/%d/',verbose_name='تصویر')
	description=models.TextField(verbose_name='متن')
	published=models.DateTimeField(default=timezone.now,verbose_name='تاریخ انتشار')
	created=models.DateTimeField(auto_now_add=True)
	updated=models.DateTimeField(auto_now=True)
	is_publish=models.CharField(choices=PUBLISH_CHOICES,default='d',max_length=1,verbose_name='وضعیت انتشار')
	hit=models.ManyToManyField(IPAddressModel,through='HitDate',verbose_name='بازدید')
	is_special=models.BooleanField(default=False,verbose_name='مقاله ویژه')

	class Meta:
		ordering = ['-published',]
		verbose_name='مقاله'
		verbose_name_plural='مقالات'


	def __str__(self):
		return self.title



class HitDate(models.Model):
	article=models.ForeignKey(BlogModel,on_delete=models.CASCADE)
	ip=models.ForeignKey(IPAddressModel,on_delete=models.CASCADE)
	created=models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return 'hitdate'
