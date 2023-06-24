from django import forms

class AddToCartForm(forms.Form):
    good_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1)

class RemoveFromCartForm(forms.Form):
    cart_item_id = forms.IntegerField(widget=forms.HiddenInput())