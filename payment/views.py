import logging
from accounts.models import ShoppingCart
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import HttpResponse, Http404


def go_to_gateway(request, id):
    cart = ShoppingCart.objects.get(
        id=id,
        owner=request.user,
    )
    if (
            request.user == cart.owner and
            request.user.is_authenticated
    ):
        amount = cart.total
        user_mobile_number = cart.owner.phone_number

        factory = bankfactories.BankFactory()
        try:
            bank = factory.auto_create()
            bank.set_request(request)
            bank.set_amount(amount)
            bank.set_mobile_number(user_mobile_number)

            bank_record = bank.ready()

            return bank.redirect_gateway()
        except AZBankGatewaysException as e:
            logging.critical(e)
            raise e


def call_back_gateway(request, id):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    cart = ShoppingCart.objects.get(
        id=id,
        owner=request.user,
    )
    if (
            request.user == cart.owner and
            request.user.is_authenticated
    ):
        if not tracking_code:
            raise Http404

        try:
            bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
        except bank_models.Bank.DoesNotExist:
            raise Http404

        if bank_record.is_success:
            cart.is_paid = True
            cart.save()
            return HttpResponse("Payment was successful.")

        return HttpResponse(
            """
            Payment has failed.
            If the money is low,
            the money will be returned to your account within 48 hours.
            """
        )
