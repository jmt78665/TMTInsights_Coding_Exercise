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


class OrderListByTagNameView(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        tags = request.data.get("tags", [])
        if len(tags) < 1:
            return Response({"error": "Need atleast one tag"}, status=400)
        orders = self.get_queryset(tags)
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data, status=200)

    def get_queryset(self, tags):
        return self.queryset.filter(tags__name__in=tags).distinct()


class ListTagsOnOrder(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderTagSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        order = self.get_queryset(id=kwargs['id'])
        serializer = self.serializer_class(order.tags, many=True)
        return Response(serializer.data, status=200)

    def get_queryset(self, **kwargs):
        return self.queryset.get(**kwargs)


class DeactivateOrderView(APIView):

    def patch(self, request: Request, *args, **kwargs) -> Response:
        try:
            order = Order.objects.get(id=kwargs['order_id'])
        except Exception as e:
            return Response({'error': str(e)}, status=400)

        order.is_active = False
        order.save()

        return Response({"msg": "Order successfully deactivated"}, status=201)


class OrdersListView(APIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        orders = self.get_queryset(**kwargs)
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data, status=200)

    def get_queryset(self, **kwargs):
        return self.queryset.filter(
            start_date__gte=kwargs["start_date"], embargo_date__lte=kwargs["embargo_date"]
        )
