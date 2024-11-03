from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.views.generic import FormView
# from .forms import CustomAuthenticationForm


class LoginView(LoginView):
    # form_class = CustomAuthenticationForm
    def form_valid(self, form):
        # کاربر را وارد کنید
        # login(self.request, form.get_user())
        messages.success(self.request, "شما با موفقیت وارد سایت شدید.")
        return super().form_valid(form)

    def form_invalid(self, form):
        # پرینت ارورهای فرم
        print("Form validation failed. Here are the errors:")
        for field in form:
            for error in field.errors:
                print(f"Error in field '{field.label}': {error}")
        for error in form.non_field_errors():
            print(f"Non-field error: {error}")

        # ادامه‌ی عملکرد پیش‌فرض
        return super().form_invalid(form)


class LogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "شما با موفقیت از سایت خارج شدید.")
        return super().dispatch(request, *args, **kwargs)


class RegisterView(FormView):
    template_name = "registration/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "ثبت نام با موفقیت انجام شد")
        return super().form_valid(form)
