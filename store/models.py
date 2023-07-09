from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    password = models.CharField(max_length=128)
    groups = models.ManyToManyField(Group, related_name='store_users', blank=True)
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='store_users',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for the user.',
        error_messages={
            'null': 'This field cannot be null.',
            'blank': 'This field cannot be blank.',
        },
    )
        
    def __str__(self):
        return self.username
    
class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image_url = models.URLField()
    description = models.TextField()
    price = models.IntegerField()
    comments = models.ManyToManyField('Comment', related_name='products', blank=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.text}'
