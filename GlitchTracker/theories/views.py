from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Theory

class TheoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Theory
    fields = ['title', 'explanation']
    template_name = 'theories/theory_form.html'

    def test_func(self):
        theory = self.get_object()
        return self.request.user == theory.author

    def get_success_url(self):
        return reverse_lazy('anomaly_detail', kwargs={'pk': self.object.anomaly.pk})

class TheoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Theory
    template_name = 'theories/theory_confirm_delete.html'

    def test_func(self):
        theory = self.get_object()
        return self.request.user == theory.author

    def get_success_url(self):
        return reverse_lazy('anomaly_detail', kwargs={'pk': self.object.anomaly.pk})
def theory_list(request):
    theories = Theory.objects.all()

    return render(request, "theories/list.html", {
        "theories": theories
    })