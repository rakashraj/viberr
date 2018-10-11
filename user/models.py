from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

gender_tup=(
    ('M','Male'),
    ('F','Female')
    )
religion_tup=(
    ('Hi','Hindu'),
    ('Mu','Muslim'),
    ("Ch","Christian"),
    ('Si','Sikh'),
    ('Bd','Buddhist'),
    ('No','No Religion'),
    ('Ot','Other')

    )
language_tup=(
    ('Hd','Hindi'),
    ('Be','Bengali'),
    ('En','English'),
    ('Ur','Urdu'),
    ('Pu','Punjabi'),
    ('Te','Telugu'),
    ('Ta','Tamil'),
    )

class MyUserManager(BaseUserManager):
    def create_user(self, email,last_Name,gender,mother_Tongue,religion,first_Name, date_of_birth,phone_No, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not first_Name:
            raise ValueError('Users must have an Name')

        user = self.model(

            email=self.normalize_email(email),
            first_Name=first_Name,  ###########################3
            religion=religion,
            mother_Tongue=mother_Tongue,
            last_Name=last_Name,
            gender=gender,
            phone_No=phone_No,
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, first_Name,last_Name,religion,mother_Tongue,gender,date_of_birth,phone_No, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,    ################################
            first_Name,
            last_Name,
            religion,
            mother_Tongue,
            gender,
            phone_No=phone_No,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    last_Name=models.CharField(max_length=30, null=True,    blank=True)
    first_Name=models.CharField(max_length=30, default=None)
    gender=models.CharField(max_length=1,choices=gender_tup, default='M')
    mother_Tongue= models.CharField(choices=language_tup, max_length=2,default='Hi')
    religion=models.CharField(choices=religion_tup,max_length=2,default=None)
    phone_No=PhoneNumberField(default=None)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
###############3
    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_Name','gender','mother_Tongue','phone_No','religion','date_of_birth','first_Name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin    