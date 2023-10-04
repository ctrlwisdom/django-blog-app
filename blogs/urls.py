from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('posts/', views.post_list),
    path('<slug:slug>', views.post_detail, name='post-detail'),
    path('category/', views.category_list, name='category'),
    path('category/<slug:slug>', views.category_detail, name='category-detail'),
    path('/tags/<slug:slug>', views.tagged, name='tag'),
    path('search/', views.search, name="search")
]
