from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


class Profile(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = 'accounts/profile.html'
    fields = ['first_name', 'last_name', 'email']

    success_url = '/accounts/profile'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        if "onboarding" in self.request.session:
            self.request.session.pop("onboarding")
            self.success_url = reverse("dashboard:index")

        return super().form_valid(form)
