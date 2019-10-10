from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:page_id>/', views.index, name='index'),
    path('waiting/', views.waiting, name='waiting'),
    path('waiting/<int:page_id>/', views.waiting, name='waiting'),
    path('best/', views.best, name='best'),
    path('best/<int:page_id>/', views.best, name='best'),
    path('random/', views.random_text, name='random'),
    path('show/<int:text_id>/', views.show, name='show'),
    path('get_image/<int:text_id>/', views.get_image, name='get_image'),
    path('vote/<plus_or_minus>/<int:text_id>/', views.vote, name='vote'),
    path('add/', views.add, name='add'),
    path('edit/<int:text_id>/', views.edit, name='edit'),
    path('publish/<int:text_id>/', views.publish, name='publish'),
    path('unpublish/<int:text_id>/', views.unpublish, name='unpublish'),
    path('remove/<int:text_id>/', views.remove, name='remove'),
]
