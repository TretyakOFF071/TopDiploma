from django.contrib.auth.models import User
from django.db import models
from django.db.models import F


class Customer(models.Model):
    """Модель покупателя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='покупатель')
    birthday = models.DateField(verbose_name='birthdate')
    phone = models.CharField(max_length=11)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f'{self.user.email}'

    class Meta:

        db_table = 'Customers'
        verbose_name = 'покупатель'
        verbose_name_plural = 'покупатели'


class Employee(models.Model):
    """Модель сотрудника"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f'{self.user.email}'

    class Meta:
        db_table = 'Employees'
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class GoodCategory(models.Model):

    name = models.CharField(verbose_name='категория товара', max_length=50,
                            db_index=True)

    class Meta:

        db_table = 'category'
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


    def __str__(self):
        return f'{self.name}'


class Provider(models.Model):

    name = models.CharField(max_length=50, verbose_name='поставщик')
    phone_number = models.CharField(max_length=11, verbose_name='телефон поставщика')
    email = models.EmailField(max_length=50, verbose_name='почта')
    contact_person = models.CharField(max_length=255, verbose_name='контактное лицо')
    categories = models.ManyToManyField(GoodCategory, verbose_name='категории')

    class Meta:

        db_table = 'providers'
        verbose_name = 'поставщик'
        verbose_name_plural = 'поставщики'

    def __str__(self):
        return f'{self.name}'

class Good(models.Model):

    name = models.CharField(max_length=25, db_index=True,
                            verbose_name='название товара')
    category = models.ForeignKey(GoodCategory, on_delete=models.CASCADE,
                                 verbose_name='категория',
                                 null=True)

    selling_price = models.FloatField(verbose_name='цена продажи')
    purchase_price = models.FloatField(verbose_name='закупочная цена')
    description = models.TextField(verbose_name='описание товара')
    image = models.ImageField(upload_to='goods/',
                              verbose_name='картинка товара',blank=True, null=True)
    quantity = models.IntegerField(verbose_name='кол-во товара')
    sold_quantity = models.IntegerField(default=0, verbose_name='кол-во продано')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, verbose_name='поставщик')
    activity_choices = [
        ('a', 'Aктивный'),
        ('i', 'Стоп-лист')
    ]

    activity_flag = models.CharField(choices=activity_choices, max_length=1,
                                     default='i', verbose_name='флаг активности')

    def add_quantity(self, num):
        Good.objects.select_for_update().only('quantity ').\
            filter(pk=self.pk).update(quantity=F('quantity ') + num)

    def sub_quantity(self, num):
        Good.objects.select_for_update().only('quantity ').\
            filter(pk=self.pk).update(quantity=F('quantity ') - num)

    def sell(self, num):
        Good.objects.select_for_update().only('sold_quantity').filter(pk=self.pk).update(sold_quantity=F('sold_quantity') + num)

    class Meta:

        db_table = 'good'
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return f'{self.name}'

class GoodCart(models.Model):

    user = models.ForeignKey(User, verbose_name='пользователь', on_delete=models.CASCADE)
    good = models.ForeignKey(Good, verbose_name='товар', on_delete=models.CASCADE)
    good_num = models.PositiveIntegerField(default=1, verbose_name='кол-во')
    payment_choices = [
        ('p', 'Оплачен'),
        ('n', 'Не оплачен')
    ]
    payment_flag = models.CharField(choices=payment_choices, max_length=1,
                                    default='n', verbose_name='статус оплаты')

    class Meta:
        db_table = 'good2cart'
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

    def __str__(self):
        return f'{self.good.name}'

class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='пользователь')

    date = models.DateTimeField(auto_now_add=True, verbose_name='дата заказа')
    cart_good = models.ManyToManyField(GoodCart, verbose_name='товар из корзины')
    amount = models.FloatField(default=0, verbose_name='общая стоимость')

    class Meta:

        db_table = 'order'
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
