from django.urls import path, include
from rest_framework import routers
from . import views

router=routers.DefaultRouter()
router.register(r'posts',views.PostViewSet)

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('api/', include(router.urls)),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<pk>', views.get_excel, name='get_excel'),
    path('post/', views.get_excel_li, name='get_excel_li'),
]