from django.urls import path

from .views import Dashboard, UpdateUserView

app_name = 'dashboard'

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard-list'),
    path('<int:pk>/update/', UpdateUserView.as_view(), name='user_update'),
]
