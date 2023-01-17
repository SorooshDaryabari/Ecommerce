from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView
from accounts.models import (
    Account,
    ShoppingCart,
    Ticket,
    CartItem,
)
from accounts.serializers import (
    AccountSerializer,
    AccountDashboardSerializer,
    ShoppingCartSerializer,
    TicketSerializer,
    CartItemSerializer,
    LoginSerializer,
)
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.http import Http404, JsonResponse
from django.contrib.auth import (
    get_user_model,
    authenticate,
    login,
    logout,
)
from accounts.permissions import (
    IsAccountOwnerOrReadOnly,
    IsOwnerOrReadOnly,
    IsCartItemOwnerOrReadOnly,
)
from rest_framework.response import Response


class AccountCreateView(CreateAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()


class AccountView(RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountDashboardSerializer
    permission_classes = (IsAuthenticated, IsAccountOwnerOrReadOnly)
    lookup_field = "username"


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        print(password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ShoppingCartListView(ListAPIView):
    serializer_class = ShoppingCartSerializer
    queryset = Ticket.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def list(self, request):
        queryset = ShoppingCart.objects.filter(owner=request.user)
        serializer = ShoppingCartSerializer(queryset, many=True)
        return Response(serializer.data)


class ShoppingCartCreateView(CreateAPIView):
    serializer_class = ShoppingCartSerializer
    queryset = ShoppingCart.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)


class ShoppingCartView(RetrieveUpdateDestroyAPIView):
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    lookup_field = "id"

    def get_queryset(self):
        user = self.request.user
        return ShoppingCart.objects.filter(owner=user)


class CartItemCreateView(CreateAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    permission_classes = (IsAuthenticated,)


class CartItemView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    permission_classes = (IsCartItemOwnerOrReadOnly, IsAuthenticated)
    lookup_field = "id"


class TicketListCreateView(ListCreateAPIView):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def list(self, request):
        queryset = Ticket.objects.filter(owner=request.user)
        serializer = TicketSerializer(queryset, many=True)
        return Response(serializer.data)


class TicketView(RetrieveUpdateDestroyAPIView):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    lookup_field = "id"


def activate_account(request, email_activate_code):
    user = get_user_model().objects.get(email_unique_code__iexact=email_activate_code)

    if user is not None:
        user.is_active = True
        user.email_unique_code = get_random_string(255)
        user.save()
        return JsonResponse({"success": "Account activated successfully."})

    else:
        raise Http404


def logout_view(request):
    logout(request)
