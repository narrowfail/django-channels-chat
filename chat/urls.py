from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('admin/', admin.site.urls),

    path('', include('core.urls')),

    path('login/', auth_views.login, name='login'),

    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout', )

]
