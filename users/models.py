from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Введите адрес электронной почты.')
        if not username:
            raise ValueError('Введите имя пользователя.')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    class UserRole(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    first_name = models.CharField(verbose_name='Имя', null=True, blank=True,
                                  max_length=100)
    last_name = models.CharField(verbose_name='Фамилия',
                                 null=True,
                                 blank=True,
                                 max_length=100)
    username = models.CharField(max_length=100,
                                unique=True,
                                null=True,
                                blank=True)
    bio = models.TextField(verbose_name='О себе', null=True, blank=True)
    email = models.EmailField(verbose_name='Адрес электронной почты',
                              unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER
    )

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    class Meta:
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.role == self.UserRole.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.UserRole.MODERATOR

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
