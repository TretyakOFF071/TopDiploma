from django.contrib.auth.models import User
from django.db import models
from django.db.models import F


class Profile(models.Model):
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

    selling_price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='цена продажи')
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='закупочная цена')
    description = models.TextField(verbose_name='описание товара')
    image = models.ImageField(upload_to='goods/',
                              verbose_name='картинка товара',blank=True, null=True)
    quantity = models.IntegerField(verbose_name='кол-во товара', default=0)
    sold_quantity = models.IntegerField(default=0, verbose_name='кол-во продано')
    manufacturer = models.CharField(max_length=30, verbose_name='производитель')

    def new_supply(self, num):
        self.quantity = F('quantity') + num
        self.save(update_fields=['quantity'])

    def make_sale(self, num):
        self.quantity = F('quantity') - num
        self.sold_quantity = F('sold_quantity') + num
        self.save(update_fields=['quantity', 'sold_quantity'])


    class Meta:

        db_table = 'good'
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return f'{self.name}'



class Supply(models.Model):
    supply_date = models.DateTimeField(auto_now_add=True)
    goods = models.ManyToManyField('Good', through='SupplyGood')
    provider = models.ForeignKey('Provider', on_delete=models.CASCADE, verbose_name='поставщик')

    class Meta:
        db_table = 'supplies'
        verbose_name = 'поставка'
        verbose_name_plural = 'поставки'

    def __str__(self):
        return f'Поставка от {self.supply_date}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for supply_good in self.supplygood_set.all():
            supply_good.good.new_supply(supply_good.quantity)
            supply_good.good.save()

    def total_cost(self):
        return sum(good.total_cost() for good in self.supplygood_set.all())

class SupplyGood(models.Model):
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE)
    good = models.ForeignKey('Good', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.good.new_supply(self.quantity)

    def total_cost(self):
        return self.good.purchase_price * self.quantity

class Sale(models.Model):
    goods = models.ManyToManyField('Good', through='SaleItem')
    sale_date = models.DateTimeField(auto_now_add=True, verbose_name='дата продажи')
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='скидка (в процентах)')
    payment_method = models.CharField(max_length=50, default='Наличные', choices=[('Наличные', 'Наличные'), ('Карта', 'Карта')], verbose_name='способ оплаты')
    final_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='итоговая стоимость', default=0)

    def total_cost(self):
        return sum(item.total_cost() for item in self.saleitem_set.all())

    def final_cost_with_discount(self):
        return self.total_cost() * (1 - self.discount / 100)

    def save(self, *args, **kwargs):
        self.final_cost = self.final_cost_with_discount()
        super().save(*args, **kwargs)
    class Meta:
        db_table = 'sales'
        verbose_name = 'продажа'
        verbose_name_plural = 'продажи'

    def __str__(self):
        return f'Продажа от {self.sale_date}'



class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    good = models.ForeignKey('Good', on_delete=models.CASCADE, verbose_name='товар')
    quantity = models.PositiveIntegerField(verbose_name='количество')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.good.make_sale(self.quantity)

    def total_cost(self):
        return self.good.selling_price * self.quantity
    class Meta:
        db_table = 'sold_goods'
        verbose_name = 'проданный товар'
        verbose_name_plural = 'проданные товары'

    def __str__(self):
        return f'{self.good.name} ({self.quantity} шт.)'