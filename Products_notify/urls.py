from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
urlpatterns = [
    path("",views.index,name="index"),
    path("login",views.login,name="login"),
    path("add_products",views.add_products,name="add_products"),
    path("logout",views.logout,name="logout"),
    path("mail_send",views.mail_send,name="mail_send"),
    path("delete/<int:id>",views.delete,name="delete"),
    path("search",views.search,name="search"),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)