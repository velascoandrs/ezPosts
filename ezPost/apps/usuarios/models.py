from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import User, PermissionsMixin, AbstractUser, UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Afinidad(models.Model):
    nombre_afinidad = models.CharField(max_length=25)

    def __str__(self):
        return '{}'.format(self.nombre_afinidad)


class Perfil(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    foto_perfil = models.ImageField(default='ninguna', upload_to='avatars', null=True, blank=True)
    foto_perfil_portada = models.ImageField(null=True, blank=True, default="defecto", upload_to='perfil_portada_imgs')
    afinidades = models.ManyToManyField(Afinidad, blank=False, related_name='Perfiles')
    fecha_nacimiento = models.DateField(null=True, blank=True)
    email_esta_confirmado = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.user.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
    instance.perfil.save()

#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
 #   instance.perfil.save()

