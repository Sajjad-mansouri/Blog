from django.shortcuts import render,redirect
from django.core import mail
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.contrib import auth
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q
from .forms import ContactForm,CustomUserCreation,MyLoginForm,BlogForm,UserInfoForm
from django.conf import settings
from blog.models import BlogModel
from .models import User


def user_info(request,user_id):
	obj=User.objects.get(id=user_id)
	form=UserInfoForm(instance=obj)
	if request.method == 'POST':
		form=UserInfoForm(request.POST,request.FILES,instance=obj)
		if form.is_valid():
			form.save()
			messages.success(request,'changed succussfully')

	context={'form':form}
	return render(request,'registration/user_info.html',context)

@login_required
def search_admin(request):
	search=request.GET.get('search')
	articles=BlogModel.objects.filter(Q(title__icontains=search)|Q(description__contains=search))
	context={'articles':articles}
	return render(request,'registration/profile.html',context)


def register(request):
	if request.method == 'POST':
		form=CustomUserCreation(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False	
			user.save()
			password_token=PasswordResetTokenGenerator()		
			current_site = get_current_site(request)
			mail_subject = 'Activate your account.'
			message = render_to_string('registration/email_template.html', {
						'user': user,
						'domain': current_site.domain,
						'uidb': urlsafe_base64_encode(force_bytes(user.pk)),
						'token': password_token.make_token(user),
					})
			to_email = form.cleaned_data.get('email')
			email = mail.EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])
			email.send()
					
			messages.success(request,'verification email sent to you')
			return redirect('login')
			
			
	else:
		form=CustomUserCreation()
	return render(request,'registration/register.html',{'form':form})

def activate(request,uidb64,token):
	User = get_user_model()
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	password_token=PasswordResetTokenGenerator()	
	active=password_token.check_token(user,token)
	if active:
		user = User.objects.get(pk=uid)
		user.is_active = True
		user.save()
		messages.success(request,'you successfuly registed')
		return redirect('profile')
	else:
		return redirect('register')


def contact(request):
	form=ContactForm()
	if request.method == 'POST':
		form=ContactForm(request.POST)
		if form.is_valid():

			subject=form.cleaned_data['subject']
			message=form.cleaned_data['message']
			sender=form.cleaned_data['email']
			name=form.cleaned_data['name']
			email = mail.EmailMessage(
			subject,
			f'hi {name}, thank you for commmenting',
			'from@example.com',
			['to1@example.com']
			)
			
			email.send() 
			messages.success(request, 'thank you for commenting ,your message recieved')
			return redirect('contact')


	return render(request,'blog/contact.html',{'form':form})
	

@login_required
def profile(request):
	if request.user.is_superuser:
		articles=BlogModel.objects.all()
	else:
		articles=BlogModel.objects.filter(author=request.user)
	context={'articles':articles}
	return render(request,'registration/profile.html',context)
@login_required
def create_article(request):
	form=BlogForm()
	if request.method=='POST':
		form=BlogForm(request.POST,request.FILES)
		if form.is_valid():
			is_publish=form.cleaned_data['is_publish']
			form=form.save(commit=False)
			if not request.user.is_superuser:
				if is_publish not in ['d','i']:
					form.is_publish='d'
			form.author=request.user
			form.save()
			return redirect('profile')

	context={'form':form}
	return render(request,'registration/create_update_article.html',context)

@login_required
def update_article(request,single_id):

		obj=get_object_or_404(BlogModel,id=single_id)
		form=BlogForm(instance=obj)

		if request.method == 'POST':
			form=BlogForm(request.POST,request.FILES,instance=obj)
			if form.is_valid():
				is_publish=form.cleaned_data['is_publish']
				form=form.save(commit=False)
				if not request.user.is_superuser:
					if is_publish not in ['d','i']:
						form.is_publish='d'
				
				form.save()
				return redirect('profile')
					
		
		context={'form':form,'article':obj}
		return render(request,'registration/create_update_article.html',context)
	

@login_required
def delete_article(request,single_id):
	obj=get_object_or_404(BlogModel,id=single_id)
	if request.method == 'POST':
		obj.delete()
		return redirect('profile')
	




