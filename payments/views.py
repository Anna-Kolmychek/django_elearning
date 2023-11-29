from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from payments.models import Payment
from payments.serializers import PaymentSerializer
from payments.services import create_stripe_session, check_payment


class PaymentsAPIViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # Убрано из-за изменения модели платежа
    # filterset_fields = ('lesson', 'course', 'payment_type', )
    ordering_fields = ('payment_date', )

    def create(self, request, *args, **kwargs):
        request.data['session_id'], request.data['session_url'] = create_stripe_session(request.data.get('course'))
        request.data['user'] = self.request.user.pk
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        check_payment(self.queryset.filter(is_paid=False).exclude(session_id__isnull=True))
        return super().list(request, *args, **kwargs)