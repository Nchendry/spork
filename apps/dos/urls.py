from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration', views.registration),
    url(r'^register', views.register),
    url(r'^login', views.login),
    url(r'^logout', views.logout),
    url(r'^home', views.home),
    url(r'^additem', views.additem),
    url(r'^createitem', views.createitem),
    url(r'^item/(?P<item_id>\d+)', views.item),
    url(r'^wishlist/(?P<item_id>\d+)', views.addwishlist),
    url(r'^remove/(?P<item_id>\d+)', views.remove),
    url(r'^delete/(?P<item_id>\d+)', views.delete),
]