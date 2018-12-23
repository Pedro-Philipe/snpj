from django.shortcuts import redirect, render
from django.http import Http404, JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import FormView, UpdateView

from adesao.models import Usuario, Assistido, Processo

from .forms import AlterarUsuarioForm

import os
from django.conf import settings

def calendario(request):
    return render(request, 'gestao/calendario.html')

class GestaoHome(View):
    template_name = "gestao/acompanhar_prazo.html"

def alterar_situacao(request, id):
    if request.method == "POST":
        form = AlterarSituacao(
            request.POST,
            instance=Usuario.objects.get(id=id))
        if form.is_valid():
            form.save()

    return redirect('gestao:detalhar', pk=id)

# def detalhar_processo(request, id):
#     processo = Processo.objects.get(id=id)
#     return render(request, 'gestao/upload_processo.html', context={'processo':processo})

def detalhesUsuario(request, id):
    usuario = Usuario.objects.get(id=id)
    user = User.objects.get(id=id)
    return render(request, 'gestao/detalhe_usuario.html', context={'usuario':usuario, 'user':user})

def detalhesAssistido(request, id):
    assistido = Assistido.objects.get(id=id)
    return render(request, 'gestao/detalhe_assistidos.html', context={'assistido': assistido})

class EditarProcesso(UpdateView):
    template_name = 'gestao/upload_processo.html'
    model = Processo
    fields = '__all__'

    def get_success_url(self):
        return reverse('gestao:processos', args=[self.kwargs['pk']])

class ListarUsuarios(ListView):
    model = Usuario
    template_name = 'gestao/listar_usuarios.html'
    paginate_by = 15

    def get_queryset(self):
        q = self.request.GET.get('q', None)
        usuarios = Usuario.objects.all()

        if q:
            usuarios = usuarios.filter(Q(user__username__icontains=q) | Q(user__email__icontains=q))

        return usuarios

class ListarAssistido(ListView):
    model = Assistido
    template_name = 'gestao/listar_assistidos.html'
    paginate_by = 15

    def get_queryset(self):
        q = self.request.GET.get('q', None)
        assistido = Assistido.objects.all()

        return assistido

class ListarProcesso(ListView):
    model = Processo
    template_name = 'gestao/listar_processos.html'
    paginate_by = 15

    def get_queryset(self):
        q = self.request.GET.get('q', None)
        processo = Processo.objects.all()

        return processo

class AlterarUsuario(UpdateView):
    model = User
    form_class = AlterarUsuarioForm
    template_name = 'gestao/listar_usuarios.html'
    success_url = reverse_lazy('gestao:usuarios')

    def get_success_url(self):
        return reverse_lazy('gestao:usuarios')
