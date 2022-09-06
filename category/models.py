from django.db import models

class Category(models.Model):
	title=models.CharField(max_length=50)
	slug=models.SlugField(max_length=50,unique=True)
	subcategory=models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True)
	created=models.DateTimeField(auto_now_add=True)
	active=models.BooleanField(default=False)

	class Meta:
		ordering = ['subcategory_id','id']
	def __str__(self):
		return self.title
