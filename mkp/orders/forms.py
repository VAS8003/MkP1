from django import forms

from orders.models import PaymentMethod


class OrderForm(forms.Form):
    address = forms.CharField(max_length=250, label='Місто, НП, ПІБ, телефон + комент', widget=forms.Textarea(attrs={'rows': 3}))
    payment_method = forms.ModelChoiceField(queryset=PaymentMethod.objects.all(), label='Спосіб платежу')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_method'].empty_label = None
