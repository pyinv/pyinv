from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.views import generic


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"


class Profile(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = "accounts/profile.html"
    fields = ["first_name", "last_name", "email"]

    success_url = "/accounts/profile"

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        if "onboarding" in self.request.session:
            self.request.session.pop("onboarding")
            self.success_url = reverse("inventory:index")

        return super().form_valid(form)
