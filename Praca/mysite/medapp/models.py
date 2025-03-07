from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.db.models.fields import SlugField
from django.db.models.fields.files import ImageField
from django.urls import reverse


class Category(models.Model):
    """
    Model representing a product category.
    """
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the URL to the list of products belonging to this category.
        """
        return reverse('medapp:product_list_by_category', args=[self.slug])

class Product(models.Model):
    """
    Model representing a product available in the store.
    """
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="Kategoria produktu")
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,db_index=True, verbose_name="Nazwa produktu")
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank = True, verbose_name="Zdjęcie produktu")
    description = models.TextField(blank=True, verbose_name="Opis produktu")
    price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Cena za dzień")
    available = models.BooleanField(default=True, verbose_name="Dostępność")
    created = models.DateField(auto_now_add=True)
    city = models.CharField(max_length=200, default="",verbose_name="Miasto")
    quantity = models.DecimalField(max_digits=10, decimal_places=0, default=1,verbose_name="Ilość")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Returns the URL to the product details.
        """
        return reverse('medapp:product-detail', kwargs={'pk':self.pk})
    
    class Meta:
        ordering = ('name',)


class Profile(models.Model):
    """
    Model representing a user profile.
    """
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='profiles/%Y/%m/%d', blank = True)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        """
        Returns the URL to the user profile details.
        """
        return reverse('medapp:profile-detail', kwargs={'pk':self.pk})

    class Meta:
        verbose_name = 'profile'

class Contact(models.Model):
    """
    Model representing a contact form.
    """
    email_guest = models.EmailField()
    topic = models.CharField(max_length=200)
    message_text = models.TextField()

    def __str__(self):
        return self.email_guest


class Order(models.Model):
    """
    Model representing a product order by a user.
    """
    product = models.ForeignKey(Product, on_delete=DO_NOTHING)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=0)
    days = models.DecimalField(max_digits=10, decimal_places=0)
    name1 = models.CharField(max_length=200,default="")
    name2 = models.CharField(max_length=200,default="")
    phone_number =  models.CharField(max_length=15, blank=True)
    home_number = models.CharField(max_length=200, default="")
    apartment = models.CharField(max_length=200,blank=True)
    postcode = models.CharField(max_length=6,default="")
    city_name = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name1
    
    class Meta:
        verbose_name = 'order'