from django import forms
from django.core.validators import RegexValidator

class OOBEForm(forms.Form):

    title = forms.CharField(
        label='System Title',
        min_length=2,
        max_length=35,
        required=True,
    )

    inventory_org = forms.CharField(
        label='Organisation Shortcode',
        min_length=3,
        max_length=3,
        required=True,
    )