from rest_framework import serializers

from payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    session_url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Payment
        fields = '__all__'

    def get_session_url(self, obj):
        request = self.context.get('request')
        if request:
            return self.context.get('request').data.get('session_url')
        return None
