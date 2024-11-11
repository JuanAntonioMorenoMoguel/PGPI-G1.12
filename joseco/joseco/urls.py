"""
URL configuration for joseco project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    
Add an import:  from my_app import views
Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    
Add an import:  from other_app.views import Home
Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    
Import the include() function: from django.urls import include, path
Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # La URL raíz del proyecto apunta a main
    path('registro/', include('Autenticacion.urls')),
    path('iniciar_sesion/', auth_views.LoginView.as_view(template_name='inicio_sesion.html'), name='iniciar_sesion'),
    path('perfil/', include('Autenticacion.urls')),
    
]