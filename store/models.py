from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=True)
    email = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)  # path

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250, blank=True,
                             null=True, default='author@gmail.com')
    rank = models.IntegerField(blank=True, default=1)
    author_img = models.ImageField(null=True, blank=True)

    #

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.author_img.url
        except:
            url = ''
        return url


class Language(models.Model):
    language = models.CharField(max_length=250, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True)  # path

    class Meta:
        verbose_name_plural = 'language'

    def get_absolute_url(self):
        return reverse('language_list:', args=[self.slug])

    def __str__(self):
        return self.language


class Product(models.Model):
    cate = models.ForeignKey(Category, related_name='product', blank=True, on_delete=models.DO_NOTHING)

    slug = models.SlugField(max_length=255)
    created_by = models.ForeignKey(User, related_name='product_creator',
                                   on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author_name = models.ForeignKey(Author, on_delete=models.SET_NULL, blank=True, null=True)  # author of book
    image = models.ImageField(null=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    language = models.ForeignKey(Language, related_name='product_lan', blank=True, on_delete=models.DO_NOTHING)
    digital = models.BooleanField(default=False, null=True, blank=False)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Product'
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,
                                 blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=250, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitem])
        return total

    @property
    def get_cart_item(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitem])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,
                                blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,
                              blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_add = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,
                                 null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,
                              null=True)
    address = models.CharField(max_length=250, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class Team(models.Model):
    GENDER = (
        ("male", "male"),
        ("female", "female"),
        ("null", "Prefer not to respond"),
        ("non-binary", "Non-binary"),
    )
    name = models.CharField(max_length=250, blank=False
                            , null=False)
    role = models.CharField(max_length=100, default='member of team')
    gender = models.CharField(max_length=100,
                              choices=GENDER)
    email = models.CharField(max_length=250, blank=True
                             , null=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
