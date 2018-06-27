from django.conf.urls import url
# from django.contrib.auth.decorators import login_required
from adesao.views import detalhar_assistido
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sucesso-cadastro-usuario/$',
        views.sucesso_usuario,
        name='sucesso_usuario'),
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'index.html'}, name='login'),
    url(r'^sair/$', 'django.contrib.auth.views.logout',
        {'template_name': 'index.html'}, name='logout'),
    url(r'^esqueci-senha/$', 'django.contrib.auth.views.password_reset',
        {'template_name': 'password_reset.html', 'post_reset_redirect': '/'}, name='esqueci_senha'),
    url(r'^ativar/usuario/(?P<codigo>[\w]+)/$',
        views.ativar_usuario, name='ativar_usuario'),


    url(r'^home/', views.home, name='home'),
    url(r'^usuario/$', views.CadastrarUsuario.as_view(), name='usuario'),
    url(r'^faleconosco/$', views.fale_conosco, name='faleconosco'),

    # calendario
    url(r'^calendario/$', views.calendario, name='calendario'),

    url(r'^listar-eventos/$', views.ListarEventos.as_view(), name='listar_eventos'),
    url(r'^listar-assistidos/$', views.ListarAssistidos.as_view(), name='listar_assistidos'),
    url(r'^detalhes/(?P<id>\d+)/$', detalhar_assistido, name='detalhar_assistido'),

    url(r'^cadastrar-eventos/$', views.CadastrarEventos.as_view(), name='cadastrar_eventos'),
    url(r'^cadastrar-assistido/$', views.CadastrarAssistido.as_view(), name='cadastrar_assistido'),

    url(r'^dados-agenda$', views.dados_agenda, name='dados_agenda'),
    ]
