from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
import uuid
from allauth.account.models import EmailAddress

# Create your models here.

class CustomUserManager(UserManager):
  def create_user(self, email, password=None, **extra_fields):
    if not email:
      raise ValueError("The email field must be set")
    
    email = self.normalize_email(email)
    extra_fields.setdefault("username", email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user
  
  def create_superuser(self, email, password=None, **extra_fields):
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_superuser", True)

    if extra_fields.get("is_staff") is not True:
        raise ValueError("Superuser must have is_staff=True.")
    if extra_fields.get("is_superuser") is not True:
        raise ValueError("Superuser must have is_superuser=True.")

    return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
  """User model"""

  id = models.UUIDField(
    primary_key=True,
    default=uuid.uuid4,
    editable=False
  )
  
  username = models.CharField(
    _("username"), max_length=150, unique=True
  )
  
  email = models.EmailField(_("email address"), unique=True)
  phone_number = models.CharField(max_length=20, blank=True)
  
  
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = []
  
  objects = CustomUserManager()
  
  class Meta:
        db_table = "users"
        verbose_name = _("User")
        verbose_name_plural = _("Users")

  def __str__(self):
        return self.email
  
  @property
  def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
  
  @property
  def email_verified(self):
    return EmailAddress.objects.filter(
      user=self,
      verified=True
    ).exists()