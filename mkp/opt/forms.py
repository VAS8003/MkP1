from django import forms

from orders.models import Status


class OrderStatusForm(forms.Form):
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label='Статус', widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['status'] = Status.objects.get(id=1)
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)