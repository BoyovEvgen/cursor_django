from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, min_length=10, required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone_number", "password1", "password2")   #

    def clean_phone_number(self):
        phone_number: str = self.cleaned_data.get('phone_number')
        if phone_number.startswith('+'):
            phone_number.lstrip('+')
        if phone_number.startswith('0') and len(phone_number) == 10:
            phone_number = '38' + phone_number
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must be numbers only.")
        if len(phone_number) != 12:
            raise forms.ValidationError("The phone must be in the format 380696969696.")
        return phone_number

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone_number = self.cleaned_data['phone_number']

        if commit:
            user.save()
        return user
