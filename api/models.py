from django.db import models

# Create your models here.
class Vendor(models.Model):
    vendor_id = models.CharField(primary_key=True,max_length=255)
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    on_time_delivery_rate = models.FloatField(null=True) #Tracks the percentage of on-time deliveries.
    quality_rating_avg = models.FloatField(null=True) #Average rating of quality based on purchase
    average_response_time = models.FloatField(null=True) #Average time taken to acknowledge purchase orders.
    fulfillment_rate = models.FloatField(null=True) #Percentage of purchase orders fulfilled successfully.
 
    def __str__(self) -> str:
        return self.name

#This model captures the details of each purchase order and is used to calculate various
#performance metrics.
class purchaseOrder(models.Model):
    po_number = models.CharField(max_length=255) #Unique number identifying the PO.
    status= models.CharField(max_length=255) # Current status of the PO (e.g., pending, completed, canceled)
    vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE) #Link to the Vendor model.
    order_date=models.DateTimeField() #Date when the order was placed.
    delivery_date=models.DateTimeField() #Expected or actual delivery date of the order.(by vendor)
    items=models.JSONField() #Details of items ordered.
    quantity=models.IntegerField() #Total quantity of items in the PO.
    quality_rating=models.FloatField(null=True) #Rating given to the vendor for this PO() #nullable).
    issue_date=models.DateTimeField() #Timestamp when the PO was issued to the vendor.
    acknowledgment_date=models.DateTimeField(null=True) #Timestamp when the vendor acknowledged the PO. #nullable

    def __str__(self) -> str:
        return self.po_number

class Performance(models.Model):
    vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE) #Link to the Vendor model.
    date=models.DateTimeField()#Date of the performance record.
    on_time_delivery_rate=models.FloatField(null=True) # Historical record of the on-time delivery rate.
    quality_rating_avg=models.FloatField(null=True) # Historical record of the quality rating average.
    average_response_time=models.FloatField(null=True) # Historical record of the average response time.
    fulfillment_rate=models.FloatField(null=True) # Historical record of the fulfilment rate.