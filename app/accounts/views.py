from django.views import View
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.viewsets import generics
from django.http import Http404

from drf_yasg.utils import swagger_auto_schema
from app.accounts.models.users import User
from app.accounts.models.customer import Customer

from app.common import messages, utils
from app.common.views import IsSuperUserMixin
from app.accounts.tasks import generation_password
from app.common.permissions import IsAuthenticatedOwnerPermission

from .serializers.accounts import (
    SignInSerializer,
    AccountSerializer,
    AccountCreateSerializer,
    UserInfoSerializer,
)
from .serializers.forgot_password import (
    ForgotPasswordSerializer,
    ResetPasswordWithTokenSerializer,
    UserChangePasswordSerializer,
)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer

    @swagger_auto_schema(
        query_serializer=SignInSerializer,
        responses={status.HTTP_200_OK: SignInSerializer()},
    )
    def post(self, request: Request, **kwargs) -> Response:
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ForgotPasswordAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer

    @swagger_auto_schema(
        query_serializer=ForgotPasswordSerializer,
        responses={status.HTTP_200_OK: ForgotPasswordSerializer()},
    )
    def post(self, request: Request, **kwargs) -> Response:
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        message = serializer.data
        status = message.pop("status")
        return Response(message, status=status)


class ResetPasswordWithToken(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordWithTokenSerializer

    @swagger_auto_schema(
        query_serializer=ResetPasswordWithTokenSerializer,
        responses={status.HTTP_200_OK: ResetPasswordWithTokenSerializer()},
    )
    def post(self, request: Request, **kwargs) -> Response:
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": messages.SUCCESS_CHANGE_PASSWORD}, status=status.HTTP_200_OK
        )


class ChangePasswordUserApiView(APIView):
    @swagger_auto_schema(
        query_serializer=UserChangePasswordSerializer,
        responses={status.HTTP_200_OK: UserChangePasswordSerializer()},
    )
    def put(self, request, **kwargs):
        serializer = UserChangePasswordSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
            return Response({"message": messages.SUCCESS_CHANGE_PASSWORD})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserInfoSerializer
    model = serializer_class.Meta.model
    queryset = Customer.objects.all()
    permission_classes = (IsAuthenticatedOwnerPermission,)

    def put(self, request: Request, **kwargs) -> Response:
        serializer = AccountSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class AccountCreateAPIView(generics.CreateAPIView):
    serializer_class = UserInfoSerializer
    model = serializer_class.Meta.model
    queryset = Customer.objects.all()
    permission_classes = (AllowAny,)

    def post(self, request: Request, **kwargs) -> Response:
        serializer = AccountCreateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.create(validated_data=serializer.validated_data)
        return Response(
            AccountCreateSerializer(data).data, status=status.HTTP_201_CREATED
        )


class AgreedAPIView(APIView):
    def get(self, request: Request, **kwargs) -> Response:
        if not request.user.agreed_at:
            ip_agent = utils.get_ip_and_agent(request)
            user = request.user
            user.agreed_agent = ip_agent.get("agent")
            user.agreed_ip = ip_agent.get("ip")
            user.agreed_at = timezone.now()
            user.save(update_fields=["agreed_agent", "agreed_ip", "agreed_at"])
        return Response({"message": "agreed"})


@method_decorator(csrf_exempt, name="dispatch")
class SendPasswordView(IsSuperUserMixin, View):
    def post(self, request):
        pk = request.POST.get("pk")
        generation_password.delay(pk)
        return JsonResponse({"status": "ok"})


class AccountMeRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserInfoSerializer
    queryset = User.objects.all()

    def get_object(self):
        pk = self.request.user.pk
        try:
            obj = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

        return obj
