from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class DeactivateOrderView(APIView):

    def patch(self, request: Request, *args, **kwargs) -> Response:
        try:
            order = Order.objects.get(id=kwargs['order_id'])
        except Exception as e:
            return Response({'error': str(e)}, status=400)

        order.is_active = False
        order.save()

        return Response({"msg": "Order successfully deactivated"}, status=201)
