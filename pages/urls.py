from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list_view, name='home'),
    path('<int:pk>/', views.post_detail_view, name='post_detail')
]