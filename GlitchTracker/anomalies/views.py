from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Anomaly
from theories.forms import TheoryForm
from .forms import RegistrationForm, AnomalyForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy

class AnomalyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Anomaly
    fields = ['title', 'description', 'location', 'danger_level', 'resolved']
    template_name = 'anomalies/anomaly_form.html'

    def test_func(self):
        anomaly = self.get_object()
        return self.request.user == anomaly.author

    def get_success_url(self):
        return reverse_lazy('anomaly_detail', kwargs={'pk': self.object.pk})

class AnomalyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Anomaly
    template_name = 'anomalies/anomaly_confirm_delete.html'
    success_url = reverse_lazy('anomaly_list')

    def test_func(self):
        anomaly = self.get_object()
        return self.request.user == anomaly.author

@login_required
def create_anomaly(request):
    if request.method == 'POST':
        form = AnomalyForm(request.POST)
        if form.is_valid():
            anomaly = form.save(commit=False)
            anomaly.author = request.user
            anomaly.save()
            return redirect('anomaly_detail', pk=anomaly.pk)
    else:
        form = AnomalyForm()
    return render(request, 'anomalies/create_anomaly.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

class AnomalyDetailView(View):
    def get(self, request, pk):
        anomaly = get_object_or_404(Anomaly, pk=pk)
        theories = anomaly.theories.all()   # теперь работает благодаря related_name
        form = TheoryForm()
        return render(request, 'anomalies/detail.html', {
            'anomaly': anomaly,
            'theories': theories,
            'form': form,
        })

    def post(self, request, pk):
        if not request.user.is_authenticated:
            return redirect('login')
        anomaly = get_object_or_404(Anomaly, pk=pk)
        form = TheoryForm(request.POST)
        if form.is_valid():
            theory = form.save(commit=False)
            theory.anomaly = anomaly
            theory.author = request.user   # если пользователь авторизован
            theory.save()
            return redirect('anomaly_detail', pk=anomaly.pk)
        theories = anomaly.theories.all()
        return render(request, 'anomalies/detail.html', {
            'anomaly': anomaly,
            'theories': theories,
            'form': form,
        })

def index(request):
    return render(request, 'anomalies/home.html')


def anomaly_list(request):
    anomalies = Anomaly.objects.all()
    return render(request, 'anomalies/list.html', {
        'anomalies': anomalies
    })

def add_to_favorites(request, pk):
    anomaly = get_object_or_404(Anomaly, pk=pk)
    favorites = request.session.get('favorites', [])
    if pk not in favorites:
        favorites.append(pk)
    request.session['favorites'] = favorites
    return redirect('anomaly_detail', pk=pk)

def remove_from_favorites(request, pk):
    favorites = request.session.get('favorites', [])
    if pk in favorites:
        favorites.remove(pk)
    request.session['favorites'] = favorites
    return redirect('favorites_list')

def favorites_list(request):
    favorites_ids = request.session.get('favorites', [])
    anomalies = Anomaly.objects.filter(id__in=favorites_ids)
    return render(request, 'anomalies/favorites.html', {'anomalies': anomalies})

def toggle_theme(request):
    theme = request.COOKIES.get('theme', 'light')
    new_theme = 'dark' if theme == 'light' else 'light'
    response = redirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie('theme', new_theme, max_age=30*24*60*60)  # 30 дней
    return response