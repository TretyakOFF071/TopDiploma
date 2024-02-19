from django.contrib.auth.models import User
from django.db import models
from django.db.models import F


class Profile(models.Model):
    """Модель пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')
    birthday = models.DateField(verbose_name='дата рождения')
    phone = models.CharField(max_length=11)

    def __str__(self):
        return f'{self.user.email}'

    class Meta:

        db_table = 'profile'
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

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
    part_number = models.CharField(max_length=10, verbose_name='артикул', default='')
    category = models.ForeignKey(GoodCategory, on_delete=models.CASCADE,
                                 verbose_name='категория',
                                 null=True)

    selling_price = models.FloatField(verbose_name='цена продажи')
    purchase_price = models.FloatField(verbose_name='закупочная цена')
    description = models.TextField(verbose_name='описание товара')
    image = models.ImageField(upload_to='goods/',
                              verbose_name='картинка товара',blank=True, null=True)
    quantity = models.IntegerField(verbose_name='кол-во товара', null=True)
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




