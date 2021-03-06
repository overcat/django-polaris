from django.utils.translation import gettext as _

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

from .forms import AllFieldsForm
from .models import PolarisStellarAccount
from polaris.utils import render_error_response


@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def all_fields_form_view(request: Request) -> Response:
    return Response(
        {
            "form": AllFieldsForm(),
            "guidance": _("This form contains every field type."),
        },
        template_name="deposit/form.html",
    )


@api_view(["GET"])
@renderer_classes([TemplateHTMLRenderer])
def confirm_email(request: Request) -> Response:
    if not (request.GET.get("token") and request.GET.get("email")):
        return render_error_response(
            "email and token arguments required.", content_type="text/html"
        )

    try:
        account = PolarisStellarAccount.objects.get(
            user__email=request.GET.get("email"),
            confirmation_token=request.GET.get("token"),
        )
    except PolarisStellarAccount.DoesNotExist:
        return render_error_response(
            "User with email and token does not exist", content_type="text/html"
        )

    account.confirmed = True
    account.save()

    return Response(template_name="email_confirmed.html")


@api_view(["GET"])
@renderer_classes([JSONRenderer])
def skip_confirm_email(request: Request) -> Response:
    account = request.session.get("account")
    try:
        account = PolarisStellarAccount.objects.get(account=account)
    except PolarisStellarAccount.DoesNotExist:
        return Response({"status": "not found"}, content_type="application/json")
    account.confirmed = True
    account.save()
    return Response({"status": "success"}, content_type="application/json")
