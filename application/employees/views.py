import io
from PIL import Image
from django.core.files.base import ContentFile
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from .models import Employee
from .forms import EmployeeForm

class EmployeeListView(ListView):
    model = Employee
    template_name = 'employees/list_employees.html'
    context_object_name = 'employees'
    paginate_by = 10  # Number of employees per page

    def get_queryset(self):
        queryset = Employee.objects.all()

        full_name_query = self.request.GET.get('full_name')
        email_query = self.request.GET.get('email')
        mobile_query = self.request.GET.get('mobile')
        date_of_birth_query = self.request.GET.get('date_of_birth')

        # Filter by name (full name) if provided
        if full_name_query:
            queryset = queryset.filter(full_name__icontains=full_name_query)

        # Filter by email if provided
        if email_query:
            queryset = queryset.filter(email__icontains=email_query)
            
        # Filter by mobile if provided
        if mobile_query:
            queryset = queryset.filter(mobile__icontains=mobile_query)

        # Filter by date_of_birth if provided
        if date_of_birth_query:
            queryset = queryset.filter(date_of_birth__icontains=date_of_birth_query)
            
        # Sorting
        sort_by = self.request.GET.get('sort_by', 'id')  # Default sort by 'full_name'
        order = self.request.GET.get('order', 'asc')
        if sort_by not in ['full_name', 'email', 'mobile', 'date_of_birth']:
            sort_by = 'id'  # Default to 'id' if invalid

        # Apply sorting direction
        if order == 'desc':
            sort_by = f'-{sort_by}'

        return queryset.order_by(sort_by)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['full_name'] = self.request.GET.get('full_name', '')
        context['email'] = self.request.GET.get('email', '')
        context['mobile'] = self.request.GET.get('mobile', '')
        context['date_of_birth'] = self.request.GET.get('date_of_birth', '')
        context['order'] = self.request.GET.get('order', 'asc')  # Add order to context
        return context

class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/add_employee.html'
    success_url = '/'  # Redirect to the employee list page after adding

    def form_valid(self, form):
        if 'photo' in self.request.FILES:
            form.instance.photo = save_resized_image(self.request.FILES['photo'])
        return super().form_valid(form)

class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'employees/edit_employee.html'
    success_url = '/'  # Redirect to the employee list page after editing

    def form_valid(self, form):
        if 'photo' in self.request.FILES:
            form.instance.photo = save_resized_image(self.request.FILES['photo'])
        return super().form_valid(form)

class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'employees/confirm_delete.html'
    success_url = '/'  # Redirect to the employee list page after deletion

def save_resized_image(image_file):
    image = Image.open(image_file)
    image = image.convert('RGB')  # Ensure image is in RGB mode
    image.thumbnail((300, 300))  # Resize the image to 300x300px or smaller

    # Save to a new file
    img_io = io.BytesIO()
    image.save(img_io, format='JPEG')
    img_content = ContentFile(img_io.getvalue(), image_file.name)
    return img_content