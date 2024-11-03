from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "ایمیل خود را وارد کنید"}
        ),
    )

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].help_text = "رمز عبور باید حداقل ۸ کاراکتر باشد."
        self.fields["password2"].help_text = (
            "تکرار گذرواژه باید مشابه گذرواژه اصلی باشد."
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("ایمیل وارد شده قبلاً ثبت شده است.")
        return email

# class CustomAuthenticationForm(AuthenticationForm):
#     email = forms.EmailField(label="ایمیل", widget=forms.EmailInput(attrs={"class": "form-control"}))

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields.pop("username")  # Remove default username field

#     def clean(self):
#         cleaned_data = super().clean()
#         email = cleaned_data.get("email")
#         if email:
#             # Map email to username for authentication
#             self.cleaned_data["username"] = email
#         return self.cleaned_data
