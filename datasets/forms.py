from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.core.validators import MinValueValidator

from datasets.models import USER


TYPES = [
    ('full_name', 'Full name'),
    ('company', 'Company'),
    ('job', 'Job'),
    ('email', 'Email'),
    ('date', 'Date'),
    ('domain_name', 'Domain name'),
    ('phone_number', 'Phone number'),
    ('address', 'Address'),
    ('integer', 'Integer'),
    ('text', 'Text')
]

COLUMN_DELIMITER = [
    (',', '(,)'),
    (';', '(;)'),
    ('\\t', '(\\t)'),
    (' ', '( )'),
    ('|', '(|)')
]

STRING_QUOTECHAR = [
    ('"', '(")'),
    (';', '(;)'),
    ('|', '(|)')
]


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

    class Meta:
        model = USER
        fields = ('username', 'password')


class CreateSchemaForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    delimiter = forms.ChoiceField(choices=COLUMN_DELIMITER, widget=forms.Select(attrs={
        'class': 'form-select'
    }))
    quotechar = forms.ChoiceField(choices=STRING_QUOTECHAR, widget=forms.Select(attrs={
        'class': 'form-select'
    }))


class ColumnSchemaForm(forms.Form):
    column_name = forms.CharField(max_length=64, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    column_type = forms.ChoiceField(choices=TYPES, widget=forms.Select(attrs={
        'class': 'form-select'
    }))
    from_value = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control'
    }), required=False)
    to_value = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control'
    }), required=False)
    order = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
    }), validators=[MinValueValidator(0)])

    def clean(self):
        cleaned_data = super().clean()
        from_value = cleaned_data.get('from_value')
        to_value = cleaned_data.get('to_value')

        if from_value is None or to_value is None:
            return cleaned_data

        if from_value < 0:
            self.add_error('from_value', 'From value cannot be negative.')
        if to_value < 0:
            self.add_error('to_value', 'To value cannot be negative.')
        if to_value <= from_value:
            self.add_error('to_value', 'To value must be greater than from value.')
        return cleaned_data
