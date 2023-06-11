from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf.urls.static import static
from django.conf import settings



from . import views

urlpatterns = [
    path("receipes/",views.receipes,name="receipe" ),
    path("delete_receipe/<id>/",views.delete_receipe,name="delete_receipe" ),
    path("update_receipe/<id>/",views.update_receipe,name="update_receipe" ),
    path("register/",views.register,name="register" ),
    path("login/",views.login_page,name="login" ),
    path("logout/",views.logout_page,name="logout" ),
]