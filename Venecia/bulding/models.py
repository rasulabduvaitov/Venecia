from django.db import models


class Flour(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    available = models.PositiveIntegerField(default=0)
    sold = models.PositiveIntegerField(default=0)
    not_fully_paid = models.PositiveIntegerField(default=0)
    reserved = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.number)


class Block(models.Model):
    name = models.CharField(max_length=5)
    flour = models.ForeignKey(Flour, related_name='blocks', on_delete=models.CASCADE)
    available = models.PositiveIntegerField(default=0)
    sold = models.PositiveIntegerField(default=0)
    not_fully_paid = models.PositiveIntegerField(default=0)
    reserved = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class House(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        SOLD = 'sold', 'Sold'
        RESERVED = 'reserved', 'Reserved'
        NOT_FULLY_PAID = 'not_fully_paid', 'Not Fully Paid'

    number = models.CharField(unique=True)
    block = models.ForeignKey(Block, related_name='houses', on_delete=models.CASCADE)
    flour = models.ForeignKey(Flour, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.AVAILABLE,
    )
    price = models.PositiveIntegerField(default=0)
    buyer_first_name = models.CharField(max_length=50, null=True, blank=True)
    buyer_last_name = models.CharField(max_length=50, null=True, blank=True)
    buyer_phone_number = models.CharField(max_length=50, null=True, blank=True)
    buyer_spend = models.PositiveIntegerField(default=0)
    how_much_is_left = models.PositiveIntegerField(default=0)

    num_in_block = models.PositiveSmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.how_much_is_left = self.price - self.buyer_spend
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.number)
