from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.IntegerField()
    email = models.EmailField()
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name