from django.shortcuts import render,HttpResponse
from .models import Employee,Role,Department
from datetime import datetime
from django.db.models import Q


# Create your views here.
def index(request):
    return render(request, 'index.html')


def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    # This line creates a dictionary called context with a key-value pair. 
    #print(context)  ----> often used for debugging purposes to see what data is being passed from the view of the template
    
    return render(request, 'all_emp.html', context)

def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = request.POST['phone']
        email = request.POST['email']
        dept_id = int(request.POST['dept'])
        role_id = int(request.POST['role'])
        hire_date = datetime.now()
        new_emp = Employee(
            first_name=first_name,
            last_name=last_name,
            salary=salary,
            bonus=bonus,
            phone=phone,
            email=email,
            dept_id=dept_id,
            role_id=role_id,
            hire_date=hire_date
        )
        new_emp.save()
        return HttpResponse('Employee added Successfully')
    elif request.method == 'GET':
        depts = Department.objects.all()
        roles = Role.objects.all()
        context = {
            'depts': depts,
            'roles': roles
        }
        return render(request, 'add_emp.html', context)
    else:
        return HttpResponse("An Exception Occurred! Employee Has Not Been Added")


def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Removed Successfully")
        except Employee.DoesNotExist:
            return HttpResponse("Please Enter A Valid EMP ID")
    else:
        emps = Employee.objects.all()
        context = {
            'emps': emps
        }
        return render(request, 'remove_emp.html', context)


def filter_emp(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        dept_id = request.POST.get('dept')
        role_id = request.POST.get('role')
        emps = Employee.objects.all()
        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept_id:
            emps = emps.filter(dept_id=dept_id)
        if role_id:
            emps = emps.filter(role_id=role_id)
        
        #the filtered queryset is stored in this dictionary
        context = {
            'emps': emps
        }
        return render(request, 'all_emp.html', context)

    elif request.method == 'GET':
        depts = Department.objects.all()
        roles = Role.objects.all()
        context = {
            'depts': depts,
            'roles': roles
        }
        return render(request, 'filter_emp.html', context)
    else:
        return HttpResponse('An Exception Occurred')