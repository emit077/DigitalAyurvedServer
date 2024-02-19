from datetime import datetime
from decimal import Decimal

from django.db import models

import choices
import keys
from drugs.models import DrugData
from helper.views import CommonHelper
from master.models import MasterVendorData
from patient.models import PatientsData


class OrderData(models.Model):
    order_id = models.CharField(max_length=255, null=True, blank=True)
    order_date = models.DateTimeField(null=True, blank=True)
    vendor = models.ForeignKey(to=MasterVendorData, on_delete=models.CASCADE, related_name='purchase_vendor', null=True,
                               blank=True)
    order_total = models.DecimalField(decimal_places=2, max_digits=11, default=Decimal(0.00), null=True, blank=True)
    transaction_type = models.CharField(max_length=20, verbose_name='transaction_type',
                                        choices=choices.TRANSACTION_TYPE_CHOICES)
    comment = models.TextField(null=True, blank=True)
    # auto
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s|%s" % (keys.TRANSACTION_DICT[self.transaction_type], self.order_id)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = "%s-%s" % (keys.TRANSACTION_DICT[self.transaction_type], datetime.today().strftime('%s'))
        return super().save(*args, **kwargs)


class OrderDetailsData(models.Model):
    drug = models.ForeignKey(to=DrugData, on_delete=models.CASCADE, related_name='purchase_drug')
    order_data = models.ForeignKey(to=OrderData, on_delete=models.CASCADE, related_name='order_data')
    quantity = models.FloatField(default=0)
    expiry_date = models.DateField(null=True, blank=True)
    unit_price = models.DecimalField(decimal_places=2, max_digits=11, default=Decimal(0.00),
                                     help_text="purchase/selling price")
    mrp = models.DecimalField(decimal_places=2, max_digits=11, default=Decimal(0.00))
    available_qty = models.FloatField(default=0)
    # auto
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class InvoiceData(models.Model):
    invoice_id = models.CharField(max_length=255, null=True, blank=True)
    patient = models.ForeignKey(to=PatientsData, on_delete=models.CASCADE, related_name='patient', null=True,
                                blank=True)
    invoice_date = models.DateTimeField(null=True, blank=True)

    item_total = models.DecimalField(decimal_places=2, max_digits=11, default=Decimal(0.00),
                                     help_text="Amount before Discount")
    invoice_total = models.DecimalField(decimal_places=2, max_digits=11, default=Decimal(0.00),
                                        help_text="Final Amount")
    round_off = models.DecimalField(decimal_places=2, max_digits=11, default=Decimal(0.00), help_text="")
    # discount
    discount_amount = models.DecimalField(decimal_places=2, max_digits=11, default=Decimal(0.00),
                                          help_text="discount amount")
    discount_value = models.DecimalField(decimal_places=2, max_digits=11, default=Decimal(0.00), help_text="")
    discount_type = models.CharField(max_length=20, verbose_name='discount_type', choices=choices.DISCOUNT_TYPE_CHOICES,
                                     default=keys.PERCENT_DISCOUNT)

    comment = models.TextField(null=True, blank=True)
    # auto
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s|%s|%s" % (self.id, self.invoice_id, self.invoice_total)

    def save(self, *args, **kwargs):
        if not self.invoice_id:
            self.invoice_id = "%s%s" % ("DA", datetime.today().strftime('%s'))
        return super().save(*args, **kwargs)


class InvoiceDetailsData(models.Model):
    drug = models.ForeignKey(to=DrugData, on_delete=models.CASCADE, related_name='invoice_drug')
    order_items = models.ForeignKey(to=OrderDetailsData, on_delete=models.CASCADE, related_name='order_items')
    invoice_data = models.ForeignKey(to=InvoiceData, on_delete=models.CASCADE, related_name='invoice_data')
    quantity = models.FloatField(default=0)
    expiry_date = models.DateField(null=True, blank=True)
    mrp = models.DecimalField(decimal_places=2, max_digits=11, default=Decimal(0.00),
                              help_text="MRP")
    selling_price = models.DecimalField(decimal_places=2, max_digits=11, default=Decimal(0.00),
                                        help_text="selling price")
    # auto
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    def subtotal(self, *args, **kwargs):
        return CommonHelper.amount_format((round(float(self.quantity) * float(self.mrp), 2)))
