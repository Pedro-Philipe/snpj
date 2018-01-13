from django.conf.urls import url
from django.contrib.auth.decorators import login_required

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
        {'template_name': 'password_reset.html', 'post_reset_redirect':'/'}, name='esqueci_senha'),
    url(r'^ativar/usuario/(?P<codigo>[\w]+)/$',
        views.ativar_usuario, name='ativar_usuario'),


    url(r'^home/', views.home, name='home'),
    url(r'^usuario/$', views.CadastrarUsuario.as_view(), name='usuario'),
    url(r'^faleconosco/$', views.fale_conosco, name='faleconosco'),

    ]
