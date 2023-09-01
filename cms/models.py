from django.db import models


class User(models.Model):
    email = models.EmailField(max_length = 254)
    password = models.CharField(max_length=50)
    fullName = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    pincode = models.CharField(max_length=6)

    class Meta:
        managed = True
        db_table = 'User'

class ContentItem(models.Model):
    title = models.CharField(max_length=30)
    body = models.CharField(max_length=300)
    summary = models.CharField(max_length=60)
    pdf = models.ImageField(upload_to='pdf')
    #categories = models.CharField(max_length=60)
    #categories = models.ManyToManyField('Category')
    author = models.ForeignKey(User,related_name='Author', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'ContentItem'

# class Category(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name
