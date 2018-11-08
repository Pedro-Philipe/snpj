import csv, json
import xlwt
import xlsxwriter
from io import BytesIO
from datetime import timedelta
from threading import Thread

from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models import Q, Count
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import pdb

from adesao.forms import CadastrarUsuarioForm,\
                         CadastrarEventosForm,\
                         CadastrarAssistidoForm,\
                         CadastroProcessoForm

from adesao.models import Usuario, Evento, Assistido, Processo
from adesao.utils import enviar_email_conclusao, verificar_anexo

# from wkhtmltopdf.views import PDFTemplateView


# Create your views here.
def index(request):
    if request.user.is_authenticated():
        return redirect('adesao:home')
    return render(request, 'index.html')


def fale_conosco(request):
    return render(request, 'fale_conosco.html')


@login_required
def home(request):

    if request.user.is_staff:
        return redirect('gestao:index')

    return render(request, 'home.html')


def ativar_usuario(request, codigo):
    usuario = Usuario.objects.get(codigo_ativacao=codigo)

    if usuario is None:
        raise Http404()

    if timezone.now() > (usuario.data_cadastro + timedelta(days=3)):
        raise Http404()

    usuario.user.is_active = True
    usuario.save()
    usuario.user.save()

    return render(request, 'confirmar_email.html')


def dados_agenda(request):
    try:
        data = serializers.serialize('json', Evento.objects.all())
        return HttpResponse(data, content_type="application/json")

    except Exception as e:
        return JsonResponse(data={"erro": True, "response": str(e)})


def sucesso_usuario(request):
    return render(request, 'usuario/mensagem_sucesso.html')


def calendario(request):
    return render(request, 'calendario.html')

def detalhar_assistido(request, id):
    assistido = Assistido.objects.get(id=id)
    return render(request, 'assistido/detalhar.html', context={'assistido':assistido})

def upload_arquivos(request, id):
    assistido = Assistido.objects.get(id=id)
    return render(request, 'assistido/upload_doc.html', context={'assistido':assistido})

class ListarEventos(ListView):
    template_name = 'agenda/listar_eventos.html'
    model = Evento
    paginate_by = 12
    

class ListarAssistidos(ListView):
    template_name = 'assistido/listar_assistidos.html'
    model = Assistido
    paginate_by = 12

class DetalheAssistido(ListView):
    model = Assistido

# class UploadDocAssistido(ListView):
#     model = Assistido
#     template_name = 'assistido/upload_doc.html'

class CadastrarEventos(CreateView):
    template_name = 'agenda/cadastrar_eventos.html'
    success_url = reverse_lazy('adesao:listar_eventos')
    model = Evento
    form_class = CadastrarEventosForm
    # fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(CadastrarEventos, self).get_context_data(**kwargs)

        if not self.request.user.is_superuser:
            context['usuarios'] = Usuario.objects.filter(id=self.request.user.id)
            return context

        context['usuarios'] = Usuario.objects.all()

        return context

class CadastrarAssistido(CreateView):
    template_name = 'assistido/cadastro_assistido.html'
    success_url = reverse_lazy('adesao:listar_assistidos')
    model = Assistido
    form_class = CadastrarAssistidoForm

# Alterar o Model depois que estiver com a tabela Processo criada
class CadastrarProcesso(CreateView):
    template_name = 'processo/criar_processo.html'
    success_url = reverse_lazy('adesao:lista_processos')
    model = Processo
    form_class = CadastroProcessoForm

    def get_context_data(self, **kwargs):
        context = super(CadastrarProcesso, self).get_context_data(**kwargs)

        context['assistidos'] = Assistido.objects.all()

        if not self.request.user.is_superuser:
            context['usuarios'] = Processo.objects.filter(id=self.request.user.id)
            return context

        context['usuarios'] = Processo.objects.all()

        return context

class ListaProcesso(ListView):
    template_name = 'processo/lista_processos.html'
    model = Processo
    paginate_by = 12

# Também deve se trocar o Model aqui, e a variavél como também troca na página de listar processo.
# Usei o Assistido como exemplo, apenas para vc ter uma ideia do fluxo
def upload_processo(request, id):
    assistido = Assistido.objects.get(id=id)
    return render(request, 'processo/upload_processo.html', context={'assistido':assistido})

def gestao_processo(request, id):
    processo = Assistido.objects.get(id=id)
    return render(request, 'processo/gestao_processo.html', context={'processo':processo})

class CadastrarUsuario(CreateView):
    form_class = CadastrarUsuarioForm
    template_name = 'usuario/cadastrar_usuario.html'
    success_url = reverse_lazy('adesao:sucesso_usuario')

    def get_success_url(self):
        Thread(target=send_mail, args=(
            'Unidesc - SNPJ - CREDENCIAIS DE ACESSO',
            'Prezad@ ' + self.object.usuario.nome_usuario + ',\n' +
            'Recebemos o seu cadastro no Sistema do Núcleos de Processos Jurídicos. ' +
            'Por favor confirme seu e-mail clicando no endereço abaixo:\n\n' +
            self.request.build_absolute_uri(reverse(
                'adesao:ativar_usuario',
                args=[self.object.usuario.codigo_ativacao])) + '\n\n' +
            'Atenciosamente,\n\n' +
            'Equipe UNIDESC',
            'naoresponda@unidesc.edu.br',
            [self.object.email],),
            kwargs={'fail_silently': 'False', }
            ).start()
        return super(CadastrarUsuario, self).get_success_url()
