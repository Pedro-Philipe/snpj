from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from . import views

urlpatterns = [
    url(r'^$', staff_member_required(
        views.ListarUsuarios.as_view(),
        login_url='adesao:login'), name='index'),

    url(r'^usuarios/',
        staff_member_required(
            views.ListarUsuarios.as_view(),
            login_url='adesao:login'), name='usuarios'),
    url(r'^alterar/usuario/(?P<pk>[\d]+)$',
        staff_member_required(
            views.AlterarUsuario.as_view(),
            login_url='adesao:login'), name='alterar_usuario'),

    # UF e Município aninhados
    url(r'^chain/municipio$', staff_member_required(views.MunicipioChain.as_view()), name='municipio_chain')

    ]
