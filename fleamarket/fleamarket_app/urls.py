from django.urls import path     
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index),
    path('jump_toLogin', views.jump_toLogin),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

    path('products', views.products),
    path('products/new', views.new),
    path('products/create', views.create),
    path('products/detail/<int:id>', views.detail),
    
    path('products/edit/<int:id>', views.edit),
    path('products/update/<int:id>', views.update),
    path('products/delete/<int:id>', views.delete), 

    # path('products/interest/<int:id>', views.interest),
    # path('products/cancel/<int:id>', views.cancel)
]
urlpatterns += staticfiles_urlpatterns()