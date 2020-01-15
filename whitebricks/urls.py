from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    path('yourads', views.yourads, name='yourads'),
    path('about', views.about, name='about'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('insert-PG', views.insert_PG, name='insert_pg'),
    path('adspace', views.adspace, name='adspace'),
    path('delete', views.delete, name='delete'),
    path('edit', views.edit, name='edit'),
    path('account_activation_sent', views.account_activation_sent, name='account_activation_sent'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})',
         views.activate, name='activate'),

                  ]