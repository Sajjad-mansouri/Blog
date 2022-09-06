from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from blog.models import BlogModel
from .models import User
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime

class UserInfoForm(forms.ModelForm):
	class Meta:
		model=User
		fields=['first_name','last_name','email','avatar']
		
		
	def __init__(self,*args,**kwargs):
		
		
		super().__init__(*args,**kwargs)

		self.fields['first_name'].widget.attrs.update({'class':"form-control"})
		self.fields['last_name'].widget.attrs.update({'class':"form-control"})
		self.fields['email'].widget.attrs.update({'class':"form-control",'required':True})
		self.fields['avatar'].widget.attrs.update({'class':"form-control"})
		



		
class ContactForm(forms.Form):
	name=forms.CharField(max_length=100)
	subject = forms.CharField(max_length=100)
	message = forms.CharField(widget=forms.Textarea)
	email = forms.EmailField()
	name.widget.attrs.update({'class': 'form-control p-4','required':"required",'placeholder':"Your Name"})
	email.widget.attrs.update({'class': 'form-control p-4','required':"required",'placeholder':"Your Email"})
	message.widget.attrs.update({'class': 'form-control ','required':"required",'placeholder':"Your message"})
	subject.widget.attrs.update({'class': 'form-control p-4','required':"required",'placeholder':"Your subject"})

class CustomUserCreation(UserCreationForm):
	class Meta:
		model=User
		fields=('username','email','first_name','last_name','password1','password2')

	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['first_name'].widget.attrs.update({'class':"form-control form-control-lg",'placeholder':" first name"})
		self.fields['last_name'].widget.attrs.update({'class':"form-control form-control-lg",'placeholder':" last Name"})

		self.fields['username'].widget.attrs.update({'class':"form-control form-control-lg",'placeholder':"username"})
		self.fields['email'].widget.attrs.update({'class':"form-control form-control-lg",'placeholder':"email",'required':True})
		self.fields['password1'].widget.attrs.update({'class':"form-control form-control-lg",'placeholder':"password"})
		self.fields['password2'].widget.attrs.update({'class':"form-control form-control-lg",'placeholder':"Retype password"})

	def clean(self):
		super().clean()
		email = self.cleaned_data.get("email")
		username=self.cleaned_data.get('username')
		if User.objects.filter(email=email).exists():
			raise ValidationError("Email exists")
		if User.objects.filter(username=username).exists():
			raise ValidationError("username exists")
		return self.cleaned_data

class MyLoginForm(forms.ModelForm):
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	class Meta:
		model=User
		fields=('username','password')

	def __init__(self, *args, **kwargs):
		super().__init__( *args, **kwargs)
		self.fields['username'].widget.attrs.update({'class':"form-control p-4",'placeholder':"email",'required':True})
		self.fields['password'].widget.attrs.update({'class':"form-control p-4",'placeholder':"password"})




class BlogForm(forms.ModelForm):
	is_special=forms.CheckboxInput()

	
	class Meta:
		model=BlogModel
		fields=['title','slug','category','image','description','is_publish','is_special']
		exclude=('author',)
		
	def __init__(self,*args,**kwargs):
		
		
		super().__init__(*args,**kwargs)
		self.fields['title'].widget.attrs.update({'class':"form-control",'placeholder':"title",'required':True})
		self.fields['slug'].widget.attrs.update({'class':"form-control",'placeholder':"slug",'required':True})
		self.fields['description'].widget.attrs.update({'class':"form-control",'placeholder':"description",'id':"summernote",'required':True})
		self.fields['is_publish'].widget.attrs.update({'class':"form-select",'required':True})
		self.fields['is_special'].widget.attrs.update({'class':"form-check-input"})

		self.fields['category'].widget.attrs.update({'class':"form-select",'required':True})	
		self.fields['image'].widget.attrs.update({'class':"form-control"})

		


