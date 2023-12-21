from django.shortcuts import render

# Create your views here.
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Vendor,purchaseOrder,Performance
from rest_framework.response import Response
from .serializers import VendorSerializer,purchaseOrderSerializer,PerformanceSerializer
from django.shortcuts import get_object_or_404
import datetime

 
@api_view(['POST'])
def vendors(request):
    vendor = VendorSerializer(data=request.data)
    # validating for already existing data
    if Vendor.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
 
    if vendor.is_valid():
        vendor.save()
        return Response(vendor.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def all_vendors(request):
    # checking for the parameters from the URL
    if request.query_params:
        vendors = Vendor.objects.filter(**request.query_params.dict())
    else:
        vendors = Vendor.objects.all()
 
    # if there is something in vendors else raise error
    if vendors:
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_vendor(request,vendor_id):
    vendor = Vendor.objects.get(vendor_id=vendor_id)
        # if there is something in vendor else raise error
    if vendor:
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
           

@api_view(['PUT'])
def update_vendors(request, vendor_id):
    vendor = Vendor.objects.get(vendor_id=vendor_id)
    data = VendorSerializer(instance=vendor, data=request.data)
 
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_vendors(request, vendor_id):
    vendor = get_object_or_404(Vendor, vendor_id=vendor_id)
    vendor.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
def create_purchase_orders(request):
    po = purchaseOrderSerializer(data=request.data)
    # validating for already existing data
    if purchaseOrder.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')
 
    if po.is_valid():
        po.save()
        return Response(po.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def all_purchase_orders(request):
    # checking for the parameters from the URL
    if request.query_params:
        purchase_orders = purchaseOrder.objects.filter(**request.query_params.dict())
    else:
        purchase_orders = purchaseOrder.objects.all()
 
    # if there is something in purchase_orders else raise error
    if purchase_orders:
        serializer = purchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_purchase_order(request,po_number):
    po = purchaseOrder.objects.get(po_number=po_number)
        # if there is something in po else raise error
    if po:
        serializer = purchaseOrderSerializer(po)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_purchase_orders(request, po_number):
    po = purchaseOrder.objects.get(po_number=po_number)
    data = purchaseOrderSerializer(instance=po, data=request.data)
 
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_purchase_orders(request, po_number):
    po = get_object_or_404(purchaseOrder, po_number=po_number)
    po.delete()
    return Response(status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
def acknowledge_purchase_orders(request, po_number):
    po = purchaseOrder.objects.get(po_number=po_number)
    acknowledgment_date = request.data['acknowledgment_date']
    data = purchaseOrderSerializer(instance=po, data={'acknowledgment_date':acknowledgment_date},partial=True)
 
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def vendor_performance(request,vendor_id):
    #Average Response Time
    #Compute the time difference between issue_date and
    # acknowledgment_date for each PO, and then find the average of these times
    # for all POs of the vendor.
    response_list=[]
    po = purchaseOrder.objects.filter(vendor=vendor_id)
    if po:
        total_po = po.count()
        for x in po:
            if type(x.acknowledgment_date) is datetime.datetime and type(x.issue_date) is datetime.datetime:
                each_response_time=x.acknowledgment_date-x.issue_date
                minutes = each_response_time.total_seconds() / 60
                hours = minutes/60
                response_list.append(hours)
            else:
                continue
        response_sum = 0
        if response_list:
            for i in response_list:
                response_sum=response_sum+i
            average_response_time =  response_sum/total_po
            print(average_response_time)
        else:
            average_response_time=None
            print("All purchase orders are not Acknowledged")


        # Fulfilment Rate Average:
        # Divide the number of successfully fulfilled POs (status 'completed'
        # without issues) by the total number of POs issued to the vendor.
        fulfilment_sum=0
        for x in po:
            if x.status == 'completed':
                fulfilment_sum = fulfilment_sum+1
            else:
                continue
        if fulfilment_sum:
            fulfillment_rate=fulfilment_sum/total_po
            print(fulfillment_rate)
        else:
            fulfillment_rate=None
            print("All purchase orders are pending")

        # Quality Rating Average:
        # Updated upon the completion of each PO where a quality_rating is provided.
        # Calculate the average of all quality_rating values for completed POs of
        # the vendor.
        po_q = po.filter(status ='completed')
        total_poq = po_q.count()
        quality_rating_sum=0
        if total_poq:
            for x in po_q:
                if x.quality_rating:
                    quality_rating_sum = quality_rating_sum+x.quality_rating
                else:
                    continue
            if quality_rating_sum:
                quality_rating_avg = quality_rating_sum/total_poq
                print(quality_rating_avg)
            else:
                quality_rating_avg=None
                print("Quality Rating is not given for Completed purchase Records")        
        else:
            quality_rating_avg = None
            print("Quality Rating None for Pending purchase Records")

        # On-Time Delivery Rate:
        # Calculated each time a PO status changes to 'completed'.
        # Count the number of completed POs delivered on or before
        # delivery_date and divide by the total number of completed POs for that vendor.
        # Not implemented due to unclarity
        #...............................................................................
        updated_values = {'vendor': vendor_id,'quality_rating_avg': quality_rating_avg, 
                'average_response_time':average_response_time,
                'fulfillment_rate':fulfillment_rate,'on_time_delivery_rate':None,
                'date' : datetime.datetime.now()}
        #Implement serializers
        if Performance.objects.filter(vendor=vendor_id).exists():
            vendor_performance = Performance.objects.get(vendor=vendor_id)
            #update
            data = PerformanceSerializer(instance=vendor_performance, data=updated_values)
            if data.is_valid():
                data.save()
                return Response(data.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            #create
            vendor_performance = PerformanceSerializer(data=updated_values)
            if vendor_performance.is_valid():
                vendor_performance.save()
                return Response(vendor_performance.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response("There is no purchase order for this vendor")