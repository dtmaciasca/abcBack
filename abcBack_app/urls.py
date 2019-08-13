from django.urls import path
from . import views

urlpatterns = [

    path('create_evento/', views.postEvento, name='post_evento'),
    path('categorias/', views.getAllCategorias, name='get_categorias'),
    path('evento/<int:idEvento>', views.getDetailEvento, name='get_id_evento'),
    path('eventos/<int:idUser>', views.getAllEventos, name='get_eventos'),
    path('update_evento/<int:idEvento>', views.putEvento, name='put_evento'),
    path('delete_evento/<int:idEvento>', views.deleteEvento, name='delete_evento'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('getTokenVal/', views.getTokenVal, name='getTokenVal'),
    path('users/add/', views.postUser, name='addUser')

]