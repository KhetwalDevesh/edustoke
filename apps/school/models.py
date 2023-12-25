from django.db import models
from apps.user.models import EduUser

class School(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, blank=True)
    starting_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    fee_upto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    board = models.CharField(max_length=255, blank=True)
    classes = models.CharField(max_length=255, blank=True)
    distance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    location = models.CharField(max_length=255, blank=True)
    facilities = models.TextField(blank=True)
    classification = models.CharField(max_length=255, blank=True)
    address = models.TextField(blank=True)
    strength = models.IntegerField(blank=True, default=0)
    transportation = models.BooleanField(blank=True, default=False)
    min_admission_age = models.IntegerField(blank=True, default=0)
    reviews = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, default=0)
    images = models.ImageField(upload_to='school_images/', blank=True, null=True)
    owner = models.ForeignKey(EduUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"School {self.id}: {self.name}"

    class Meta:
        db_table = 'school'  # Specify the desired table name here


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='student_images/', blank=True, null=True)
    parent = models.ForeignKey(EduUser, on_delete=models.CASCADE)
    school_applied_for = models.CharField(max_length=255)
    class_applied_for = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    dob = models.DateField(blank=True, null=True)
    place_of_birth = models.CharField(max_length=255, blank=True)
    nationality = models.CharField(max_length=255, blank=True)
    religion = models.CharField(max_length=255, blank=True)
    caste = models.CharField(max_length=255, blank=True)
    blood_group = models.CharField(max_length=10, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    class_previously_attended = models.CharField(max_length=255, blank=True)
    reason_for_tc = models.TextField(blank=True)
    sibling_name = models.CharField(max_length=255, blank=True)
    sibling_age = models.IntegerField(blank=True, null=True)
    sibling_class = models.CharField(max_length=255, blank=True)
    sibling_school = models.CharField(max_length=255, blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    twitter = models.CharField(max_length=255, blank=True)
    skype = models.CharField(max_length=255, blank=True)
    birth_certificate = models.FileField(upload_to='birth_certificates/', blank=True, null=True)
    previous_marksheet = models.FileField(upload_to='previous_marksheets/', blank=True, null=True)
    admission_status = models.CharField(max_length=255, default='pending')

    def __str__(self):
        return f"Student {self.id}: {self.name}"

    class Meta:
        db_table = 'student'  # Specify the desired table name here
