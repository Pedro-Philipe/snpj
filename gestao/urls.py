from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required
from . import views

urlpatterns = [
    url(r'^inicio/', staff_member_required(
        views.ListarProcesso.as_view(),
        login_url='adesao:login'), name='index'),

    url(r'^calendario/$', views.calendario, name='calendario'),
    
    url(r'^usuarios/',
        staff_member_required(
            views.ListarUsuarios.as_view(),
            login_url='adesao:login'), name='usuarios'),

    url(r'^assistidos/',
        staff_member_required(
            views.ListarAssistido.as_view(),
            login_url='adesao:login'), name='assistidos'),
    url(r'^processos/',
        staff_member_required(
            views.ListarProcesso.as_view(),
            login_url='adesao:login'), name='processos'),
    url(r'^editar-processo/(?P<pk>\d+)/$', 
        staff_member_required(
            views.EditarProcesso.as_view(),
            login_url='adesao:login'), name='editar_processo'),
    url(r'^assistido/detalhes/(?P<id>\d+)/$',
        staff_member_required(
            views.detalhesAssistido,
            login_url='adesao:login'), name='detalhesAssistido'),
    url(r'^usuario/detalhes/(?P<id>\d+)/$',
        staff_member_required(
            views.detalhesUsuario,
            login_url='adesao:login'), name='detalhesUsuario'),
    url(r'^alterar/usuario/(?P<pk>[\d]+)$',
        staff_member_required(
            views.AlterarUsuario.as_view(),
            login_url='adesao:login'), name='alterar_usuario'),
]
