from django.db import models



# ------------------------------------------------------------------------- Labours Registration Details

class UserSignup(models.Model):
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    alt_mobile_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # Store hashed password in production
    address_proof = models.FileField(upload_to='uploads/')  # Save files in uploads folder

    def __str__(self):
        return self.username


#  -------------------------------------------------------------------------- Get AC Repair Labour List

class EmpOtherServiceWorker(models.Model):
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    experience = models.IntegerField()
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# ----------------------------------------------------------------------------------

class Labour(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    available_hours = models.CharField(max_length=100, null=True)
    language = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Requirement(models.Model):
    urgency = models.CharField(max_length=100)
    working_hours = models.CharField(max_length=100)
    specific_requirement = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.urgency

import os
import uuid

def upload_to(instance, filename):
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    return os.path.join("uploads/", unique_name)

class UploadedPhoto(models.Model):
    photo = models.ImageField(upload_to=upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)



# ---------------------------------------------------------------------------- Get AC Reapir Labour List




# ------------------------------------------------------  fetching baby caretaker requirement details

# api/models.py

from django.db import models

class BabyCaretakerRequirement(models.Model):
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    address = models.TextField()
    photo = models.ImageField(upload_to='photos/')
    identity_card = models.ImageField(upload_to='identity_cards/')
    child_name = models.CharField(max_length=100)
    child_age = models.IntegerField()
    child_gender = models.CharField(max_length=50)
    child_health_issues = models.TextField()
    urgency = models.CharField(max_length=50)
    preferred_care_time = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    City = models.CharField(max_length=100)
    Area = models.CharField(max_length=100)
    specific_preferences_language = models.CharField(max_length=100)
    specific_requirements = models.TextField()
    salary_offer = models.CharField(max_length=50)

    
class EmpBabyCaretaker(models.Model):
    full_name = models.CharField(max_length=255, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)
    email = models.CharField(unique=True, blank=False, null=False, max_length=255)
    address = models.CharField(max_length=255, blank=False, null=False)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)  # Optional
    identity_card = models.ImageField(upload_to='identity_cards/', blank=True, null=True)  # Optional
    username = models.CharField(unique=True, blank=False, null=False, max_length=150)
    password = models.CharField(max_length=255, blank=False, null=False)
    gender = models.CharField(max_length=100, blank=False, null=False)
    working_hours = models.CharField(max_length=50, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    area = models.CharField(max_length=100, blank=False, null=False)
    availability = models.CharField(max_length=100, blank=False, null=False)
    language = models.CharField(max_length=100, blank=False, null=False)
    hourly_rate = models.CharField(max_length=100, blank=False, null=False)
    experience = models.CharField(max_length=100, blank=False, null=False)
    specific_requirements = models.CharField(max_length=255, blank=True, null=True)  # Optional field

    def __str__(self):
        return self.full_name

    
class EmpOtherservice(models.Model):
    full_name = models.CharField(max_length=255, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)
    email = models.CharField(unique=True, blank=False, null=False, max_length=255)
    address = models.CharField(max_length=255, blank=False, null=False)
    mobilenumber = models.IntegerField(blank=True, null=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)  # Optional
    identity_card = models.ImageField(upload_to='identity_cards/', blank=True, null=True)  # Optional
    gender = models.CharField(max_length=100, blank=False, null=False)
    working_hours = models.CharField(max_length=50, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    area = models.CharField(max_length=100, blank=False, null=False)
    availability = models.CharField(max_length=100, blank=False, null=False)
    language = models.CharField(max_length=100, blank=False, null=False)
    hourly_rate = models.CharField(max_length=100, blank=False, null=False)
    experience = models.CharField(max_length=100, blank=False, null=False)
    specific_requirements = models.CharField(max_length=255, blank=True, null=True)  # Optional field

    def __str__(self):
        return self.full_name
    


class ElderCaretaker(models.Model):
    full_name = models.CharField(max_length=255, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)
    email = models.CharField(unique=True, blank=False, null=False, max_length=255)
    address = models.CharField(max_length=255, blank=False, null=False)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)  # Optional
    identity_card = models.ImageField(upload_to='identity_cards/', blank=True, null=True)  # Optional
    username = models.CharField(unique=True, blank=False, null=False, max_length=150)
    password = models.CharField(max_length=255, blank=False, null=False)
    gender = models.CharField(max_length=100, blank=False, null=False)
    working_hours = models.CharField(max_length=50, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    area = models.CharField(max_length=100, blank=False, null=False)
    availability = models.CharField(max_length=100, blank=False, null=False)
    language = models.CharField(max_length=100, blank=False, null=False)
    hourly_rate = models.CharField(max_length=100, blank=False, null=False)
    experience = models.CharField(max_length=100, blank=False, null=False)
    specific_requirements = models.CharField(max_length=255, blank=True, null=True)  # Optional field

    def __str__(self):
        return self.full_name
    

class Cleaner(models.Model):
    full_name = models.CharField(max_length=255, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)
    email = models.CharField(unique=True, blank=False, null=False, max_length=255)
    address = models.CharField(max_length=255, blank=False, null=False)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)  # Optional
    identity_card = models.ImageField(upload_to='identity_cards/', blank=True, null=True)  # Optional
    username = models.CharField(unique=True, blank=False, null=False, max_length=150)
    password = models.CharField(max_length=255, blank=False, null=False)
    gender = models.CharField(max_length=100, blank=False, null=False)
    working_hours = models.CharField(max_length=50, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    area = models.CharField(max_length=100, blank=False, null=False)
    availability = models.CharField(max_length=100, blank=False, null=False)
    language = models.CharField(max_length=100, blank=False, null=False)
    hourly_rate = models.CharField(max_length=100, blank=False, null=False)
    experience = models.CharField(max_length=100, blank=False, null=False)
    specific_requirements = models.CharField(max_length=255, blank=True, null=True)  # Optional field

    def __str__(self):
        return self.full_name
    


class Cooking(models.Model):
    full_name = models.CharField(max_length=255, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)
    email = models.CharField(unique=True, blank=False, null=False, max_length=255)
    address = models.CharField(max_length=255, blank=False, null=False)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)  # Optional
    identity_card = models.ImageField(upload_to='identity_cards/', blank=True, null=True)  # Optional
    username = models.CharField(unique=True, blank=False, null=False, max_length=150)
    password = models.CharField(max_length=255, blank=False, null=False)
    gender = models.CharField(max_length=100, blank=False, null=False)
    working_hours = models.CharField(max_length=50, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    area = models.CharField(max_length=100, blank=False, null=False)
    availability = models.CharField(max_length=100, blank=False, null=False)
    language = models.CharField(max_length=100, blank=False, null=False)
    hourly_rate = models.CharField(max_length=100, blank=False, null=False)
    experience = models.CharField(max_length=100, blank=False, null=False)
    specific_requirements = models.CharField(max_length=255, blank=True, null=True)  # Optional field

    def __str__(self):
        return self.full_name
    

class Tankcleaner(models.Model):
    full_name = models.CharField(max_length=255, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)
    email = models.CharField(unique=True, blank=False, null=False, max_length=255)
    address = models.CharField(max_length=255, blank=False, null=False)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)  # Optional
    identity_card = models.ImageField(upload_to='identity_cards/', blank=True, null=True)  # Optional
    username = models.CharField(unique=True, blank=False, null=False, max_length=150)
    password = models.CharField(max_length=255, blank=False, null=False)
    gender = models.CharField(max_length=100, blank=False, null=False)
    working_hours = models.CharField(max_length=50, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    area = models.CharField(max_length=100, blank=False, null=False)
    availability = models.CharField(max_length=100, blank=False, null=False)
    language = models.CharField(max_length=100, blank=False, null=False)
    hourly_rate = models.CharField(max_length=100, blank=False, null=False)
    experience = models.CharField(max_length=100, blank=False, null=False)
    specific_requirements = models.CharField(max_length=255, blank=True, null=True)  # Optional field

    def __str__(self):
        return self.full_name
    


class Driver(models.Model):
    full_name = models.CharField(max_length=255, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)
    email = models.CharField(unique=True, blank=False, null=False, max_length=255)
    address = models.CharField(max_length=255, blank=False, null=False)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)  # Optional
    identity_card = models.ImageField(upload_to='identity_cards/', blank=True, null=True)  # Optional
    username = models.CharField(unique=True, blank=False, null=False, max_length=150)
    password = models.CharField(max_length=255, blank=False, null=False)
    gender = models.CharField(max_length=100, blank=False, null=False)
    working_hours = models.CharField(max_length=50, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    area = models.CharField(max_length=100, blank=False, null=False)
    availability = models.CharField(max_length=100, blank=False, null=False)
    language = models.CharField(max_length=100, blank=False, null=False)
    hourly_rate = models.CharField(max_length=100, blank=False, null=False)
    experience = models.CharField(max_length=100, blank=False, null=False)
    specific_requirements = models.CharField(max_length=255, blank=True, null=True)  # Optional field

    def __str__(self):
        return self.full_name
    
    
    


class EmpBabyCaretaker(models.Model):
    full_name = models.CharField(max_length=255, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)
    email = models.CharField(unique=True, blank=False, null=False, max_length=255)
    address = models.CharField(max_length=255, blank=False, null=False)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)  # Optional
    identity_card = models.ImageField(upload_to='identity_cards/', blank=True, null=True)  # Optional
    username = models.CharField(unique=True, blank=False, null=False, max_length=150)
    password = models.CharField(max_length=255, blank=False, null=False)
    gender = models.CharField(max_length=100, blank=False, null=False)
    working_hours = models.CharField(max_length=50, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    area = models.CharField(max_length=100, blank=False, null=False)
    availability = models.CharField(max_length=100, blank=False, null=False)
    language = models.CharField(max_length=100, blank=False, null=False)
    hourly_rate = models.CharField(max_length=100, blank=False, null=False)
    experience = models.CharField(max_length=100, blank=False, null=False)
    specific_requirements = models.CharField(max_length=255, blank=True, null=True)  # Optional field

    def __str__(self):
        return self.full_name
    


class EmpElderCaretaker(models.Model):
    full_name = models.CharField(max_length=255, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)
    email = models.CharField(unique=True, blank=False, null=False, max_length=255)
    address = models.CharField(max_length=255, blank=False, null=False)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)  # Optional
    identity_card = models.ImageField(upload_to='identity_cards/', blank=True, null=True)  # Optional
    username = models.CharField(unique=True, blank=False, null=False, max_length=150)
    password = models.CharField(max_length=255, blank=False, null=False)
    gender = models.CharField(max_length=100, blank=False, null=False)
    working_hours = models.CharField(max_length=50, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    area = models.CharField(max_length=100, blank=False, null=False)
    availability = models.CharField(max_length=100, blank=False, null=False)
    language = models.CharField(max_length=100, blank=False, null=False)
    hourly_rate = models.CharField(max_length=100, blank=False, null=False)
    experience = models.CharField(max_length=100, blank=False, null=False)
    specific_requirements = models.CharField(max_length=255, blank=True, null=True)  # Optional field

    def __str__(self):
        return self.full_name
    

class EmpCleaner(models.Model):
    full_name = models.CharField(max_length=255, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)
    email = models.CharField(unique=True, blank=False, null=False, max_length=255)
    address = models.CharField(max_length=255, blank=False, null=False)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)  # Optional
    identity_card = models.ImageField(upload_to='identity_cards/', blank=True, null=True)  # Optional
    username = models.CharField(unique=True, blank=False, null=False, max_length=150)
    password = models.CharField(max_length=255, blank=False, null=False)
    gender = models.CharField(max_length=100, blank=False, null=False)
    working_hours = models.CharField(max_length=50, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    area = models.CharField(max_length=100, blank=False, null=False)
    availability = models.CharField(max_length=100, blank=False, null=False)
    language = models.CharField(max_length=100, blank=False, null=False)
    hourly_rate = models.CharField(max_length=100, blank=False, null=False)
    experience = models.CharField(max_length=100, blank=False, null=False)
    specific_requirements = models.CharField(max_length=255, blank=True, null=True)  # Optional field

    def __str__(self):
        return self.full_name
    


class EmpCooking(models.Model):
    full_name = models.CharField(max_length=255, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)
    email = models.CharField(unique=True, blank=False, null=False, max_length=255)
    address = models.CharField(max_length=255, blank=False, null=False)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)  # Optional
    identity_card = models.ImageField(upload_to='identity_cards/', blank=True, null=True)  # Optional
    username = models.CharField(unique=True, blank=False, null=False, max_length=150)
    password = models.CharField(max_length=255, blank=False, null=False)
    gender = models.CharField(max_length=100, blank=False, null=False)
    working_hours = models.CharField(max_length=50, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    area = models.CharField(max_length=100, blank=False, null=False)
    availability = models.CharField(max_length=100, blank=False, null=False)
    language = models.CharField(max_length=100, blank=False, null=False)
    hourly_rate = models.CharField(max_length=100, blank=False, null=False)
    experience = models.CharField(max_length=100, blank=False, null=False)
    specific_requirements = models.CharField(max_length=255, blank=True, null=True)  # Optional field

    def __str__(self):
        return self.full_name
    

class EmpTankcleaner(models.Model):
    full_name = models.CharField(max_length=255, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)
    email = models.CharField(unique=True, blank=False, null=False, max_length=255)
    address = models.CharField(max_length=255, blank=False, null=False)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)  # Optional
    identity_card = models.ImageField(upload_to='identity_cards/', blank=True, null=True)  # Optional
    username = models.CharField(unique=True, blank=False, null=False, max_length=150)
    password = models.CharField(max_length=255, blank=False, null=False)
    gender = models.CharField(max_length=100, blank=False, null=False)
    working_hours = models.CharField(max_length=50, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    area = models.CharField(max_length=100, blank=False, null=False)
    availability = models.CharField(max_length=100, blank=False, null=False)
    language = models.CharField(max_length=100, blank=False, null=False)
    hourly_rate = models.CharField(max_length=100, blank=False, null=False)
    experience = models.CharField(max_length=100, blank=False, null=False)
    specific_requirements = models.CharField(max_length=255, blank=True, null=True)  # Optional field

    def __str__(self):
        return self.full_name
    

class EmpDriver(models.Model):
    full_name = models.CharField(max_length=255, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)
    email = models.CharField(unique=True, blank=False, null=False, max_length=255)
    address = models.CharField(max_length=255, blank=False, null=False)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)  # Optional
    identity_card = models.ImageField(upload_to='identity_cards/', blank=True, null=True)  # Optional
    username = models.CharField(unique=True, blank=False, null=False, max_length=150)
    password = models.CharField(max_length=255, blank=False, null=False)
    gender = models.CharField(max_length=100, blank=False, null=False)
    working_hours = models.CharField(max_length=50, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    area = models.CharField(max_length=100, blank=False, null=False)
    availability = models.CharField(max_length=100, blank=False, null=False)
    language = models.CharField(max_length=100, blank=False, null=False)
    hourly_rate = models.CharField(max_length=100, blank=False, null=False)
    experience = models.CharField(max_length=100, blank=False, null=False)
    specific_requirements = models.CharField(max_length=255, blank=True, null=True)  # Optional field

    def __str__(self):
        return self.full_name
    


from djongo import models

class Labour(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    area = models.CharField(max_length=100)
    skills = models.CharField(max_length=200)

    def __str__(self):
        return self.name
