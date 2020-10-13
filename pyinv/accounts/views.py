from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.views import generic
from dynamic_preferences.forms import preference_form_builder, PreferenceForm
from dynamic_preferences.users.registries import user_preferences_registry


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

        messages.success(self.request, "Your profile has been successfully updated")
        return super().form_valid(form)


class UserPreferenceForm(PreferenceForm):
    registry = user_preferences_registry

class Preferences(LoginRequiredMixin, generic.FormView):
    template_name = "accounts/preferences.html"

    success_url = "/accounts/preferences"
    
    def get_form_class(self):
        return preference_form_builder(UserPreferenceForm)

    def form_valid(self, form):
        for k, v in self.request.user.preferences.items():
            if type(v) is bool:
                self.request.user.preferences[k] = k in form.data
            else:
                self.request.user.preferences[k] = form.data[k]
        messages.success(self.request, "Your preferences have been successfully updated")
        return super().form_valid(form)