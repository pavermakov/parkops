from django.db import models


class DiscountCategory(models.Model):
    title = models.CharField(max_length=255)
    discount_percent = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = "Discount categories"

    def __str__(self):
        return f'{self.title} ({self.discount_percent}%)'
