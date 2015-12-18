from django import forms

from models import Order


class BuyShirtForm(forms.Form):
    size = forms.ChoiceField(choices=Order.SIZES, label="Choose your Size")