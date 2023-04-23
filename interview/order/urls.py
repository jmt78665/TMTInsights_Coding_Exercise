
from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView, DeactivateOrderView, OrdersListView


urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('', OrderListCreateView.as_view(), name='order-list'),
    path('deactivate-order/<int:order_id>', DeactivateOrderView.as_view(), name='deactivate-order'),
    path('orders/<str:start_date>/<str:embargo_date>', OrdersListView.as_view(), name='list-orders')
]