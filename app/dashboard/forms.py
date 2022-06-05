from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django_unifi_portal.models import UnifiUser


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name',
                  'last_name']

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        return super().form_valid(form)


class UnifiUserForm(forms.ModelForm):

    class Meta:
        model = UnifiUser
        fields = ['picture', 'gender', 'city', 'about', 'phone']

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.

        return super().form_valid(form)


UpdateUserFormset = inlineformset_factory(
    User,
    UnifiUser,
    fields=('picture', 'gender', 'city', 'about', 'phone',),
    max_num=1
)
