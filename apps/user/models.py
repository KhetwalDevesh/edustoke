from django.db import models

ROLE_CHOICES = (
    ('parent', 'Parent'),
    ('vendor', 'Vendor'),
    ('school_owner', 'SchoolOwner'),
)


class EduUser(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=50)
    roles = models.JSONField(default=list, blank=True)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=255, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    address = models.TextField(blank=True)
    fatherName = models.CharField(max_length=255, blank=True)
    fatherQualification = models.CharField(max_length=255, blank=True)
    fatherOccupation = models.CharField(max_length=255, blank=True)
    fatherIncome = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    fatherEmail = models.EmailField(blank=True)
    motherName = models.CharField(max_length=255, blank=True)
    motherQualification = models.CharField(max_length=255, blank=True)
    motherOccupation = models.CharField(max_length=255, blank=True)
    motherIncome = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
    motherEmail = models.EmailField(blank=True)

    def __str__(self):
        return f"EduUser {self.id}: {', '.join(self.roles)}"

    class Meta:
        db_table = 'edu_user'  # Specify the desired table name here
