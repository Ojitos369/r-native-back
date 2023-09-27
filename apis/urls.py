from django.urls import path, include


app_name = 'apis'
urlpatterns = [
    path('users/', include('apis.users.urls'), name=f'{app_name}_users'),
    path('login/', include('apis.login.urls'), name=f'{app_name}_login'),
    path('general/', include('apis.general.urls'), name=f'{app_name}_general'),
]