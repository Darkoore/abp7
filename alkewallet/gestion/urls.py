
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('', inicio,name='inicio'),
    path('registro/', registro,name='registro'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    
    path('cuentas/', cuenta_list,name='cuenta_list'),
    path('cuentas/nueva/', cuenta_create,name='cuenta_create'),
    path('cuentas/<int:pk>/editar/', cuenta_update,name='cuenta_update'),
    path('cuentas/<int:pk>/eliminar/', cuenta_delete,name='cuenta_delete'),

    path('transacciones/', transaccion_list,name='transaccion_list'),
    path('transacciones/create/', transaccion_create,name='transaccion_create'),

    path('reportes/', reportes,name='reportes'),

    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 


