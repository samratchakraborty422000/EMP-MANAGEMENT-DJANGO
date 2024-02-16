from django.db import models
from django.core.validators import EmailValidator,RegexValidator
from django.utils import timezone

# Create your models here.

class Department(models.Model):
    name=models.CharField(max_length=100,null=False)
    location=models.CharField(max_length=100)

    def __str__(self):
        return self.name


#Role Model
class Role(models.Model):
    name=models.CharField(max_length=100,null=False)

    def __str__(self):
        return self.name



#Employee model
class Employee(models.Model):
    first_name=models.CharField(max_length=100,null=False)
    last_name = models.CharField(max_length=100)
    salary = models.PositiveIntegerField(default=0)
    bonus = models.PositiveIntegerField(default=0)
    
    # Establishes a relationship where each instance of this model belongs to a Department
    #deletion of the related Department results in cascading deletion of associated instances.
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    
    #using validators
    phone = models.CharField(
        max_length=10, 
        null=False, 
        help_text="Enter valid phone number",
        validators=[RegexValidator(regex=r'\d{10}$',message='Phone number must contain 10 digits')],
        )  

    email=models.EmailField(
        max_length=256,
        null=False,
        validators=[EmailValidator(message="Enter a valid email address")],
        help_text="Enter a valid email address",
        )
    
    hire_date = models.DateField(default=timezone.now().date())


    class Meta:
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(salary__gte=0),
                name='salary_non_negative'
            ),
            models.CheckConstraint(
                check=models.Q(bonus__gte=0),
                name='bonus_non_negative'
            ),
            models.CheckConstraint(
                check=models.Q(hire_date__lte=timezone.now().date()),
                name='hire_date_not_future'
            ),
        ]    
    def __str__(self):
        return f"{self.first_name} {self.last_name} (Phone: {self.phone} ) (Email: {self.email}) {self.dept}"



