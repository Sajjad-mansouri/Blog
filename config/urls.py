
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views
from django.conf import settings
from django.conf.urls.static import static
from account.forms import MyLoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
path('',include('django.contrib.auth.urls')),
    path('',include('blog.urls')),
    path('',include('category.urls')),
    path('',include('account.urls')),
    
    
]
urlpatterns +=[

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
