from braces.views import AjaxResponseMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django_unifi_portal.models import UnifiUser

from .forms import UpdateUserFormset, UserForm


class Dashboard(AjaxResponseMixin, ListView):
    context_object_name = "user_list"
    template_name = "dashboard/dashboard.html"

    def get_queryset(self):
        return UnifiUser.objects.all()

    def users_registered_today(self):
        u = UnifiUser.objects.filter(created_at=timezone.now()).count()
        return u

    def statistics(self):
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_users'] = UnifiUser.objects.count()
        context['registe_today'] = self.users_registered_today()
        return context

    # @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(Dashboard, self).dispatch(request, *args, **kwargs)


class UpdateUserView(UpdateView):
    model = User
    form_class = UserForm
    template_name = "dashboard/update_user.html"

    def get_user_infor(self):
        user_data = UnifiUser.objects.get(user=self.object.pk)
        user_infor = {
            "phone": user_data.phone,
            "photo": user_data.picture.url,
        }

        return user_infor

    def get_context_data(self, **kwargs):
        context = super(UpdateUserView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['user_formset'] = UpdateUserFormset(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['user_formset'] = UpdateUserFormset(instance=self.object)
        context['user_data'] = self.get_user_infor()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        user_formset = UpdateUserFormset(self.request.POST, self.request.FILES, instance=self.object)
        if (form.is_valid() and user_formset.is_valid()):
            return self.form_valid(form, user_formset)
        else:
            return self.form_invalid(form, user_formset)

    def form_valid(self, form, user_formset):
        self.object = form.save()
        user_formset.instance = self.object
        user_formset.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, user_formset):
        return self.render_to_response(
            self.get_context_data(form=form, user_formset=user_formset))

    def get_success_url(self):
        return reverse('dashboard:user_update', kwargs={'pk': self.object.pk})
