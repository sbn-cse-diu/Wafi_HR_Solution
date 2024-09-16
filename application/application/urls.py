from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from employees.views import EmployeeListView, EmployeeCreateView, EmployeeUpdateView, EmployeeDeleteView

urlpatterns = [
    path('', EmployeeListView.as_view(), name='employee_list'),
    path('add/', EmployeeCreateView.as_view(), name='add_employee'),
    path('<int:pk>/edit/', EmployeeUpdateView.as_view(), name='edit_employee'),
    path('<int:pk>/delete/', EmployeeDeleteView.as_view(), name='delete_employee'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

