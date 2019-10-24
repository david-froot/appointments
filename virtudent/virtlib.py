from django.views.generic.edit import UpdateView, CreateView, DeleteView, FormView
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404

def group_required(group_names):
    """Requires user membership in at least one of the groups passed in."""

    if type(group_names ) == str:
        group_names = [group_names]

    def in_groups(u):
        if u.is_authenticated():
            for group in group_names:
                if group=='admin' and u.is_staff:
                    return True
                try:
                    grp = getattr(u, group)
                except Exception:
                    return False
                return True
        return False
    return user_passes_test(in_groups)


class UpdateViewUser(UpdateView):

    role = 'patient'

    def get_object(self, queryset=None):
        """
        Make sure the person who queries is the object actually owns it
        """
        obj = super(UpdateViewUser, self).get_object(queryset)
        if getattr(obj, self.role) != getattr(self.request.user, self.role):
            print 'Ownership error'
            raise Http404
        return obj

    def form_valid(self, form):
        """
        Set the owner of the object
        """
        owner = getattr(self.request.user, self.role)
        set(form.instance, self.role,  owner)
        return super(UpdateViewUser, self).form_valid(form)

class DeleteViewUser(DeleteView):

    role = 'patient'

    def get_object(self, queryset=None):
        obj = super(DeleteViewUser, self).get_object(queryset)
        if getattr(obj, self.role) != getattr(self.request.user, self.role):
            print 'Ownership error'
            raise Http404

