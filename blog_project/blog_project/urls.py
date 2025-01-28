"""
URL configuration for testing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

#Swagger
#schema_view is the interface that displays the API documentation in a graphical form.
schema_view = get_schema_view(
    #openapi.Info() function allows to set general information about my API
   openapi.Info(
      title="Blog API",
      #The API version to display
      default_version='v1',
      description="swagger of the Blog API",
      #Link to the API Terms of Use
      #Here a link to Google's Terms of Use page is provided
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="dorinafg2@gmail.com"),
      license=openapi.License(name="IDF License"),
   ),
    #Swagger UI will be available to anyone who requests it. (because it true)
   public=True,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('app_blog.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),

]