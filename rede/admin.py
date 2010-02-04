# -*- coding: utf-8 -*-
from django.contrib.admin import site, ModelAdmin
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.simple import direct_to_template, redirect_to
from django.views.decorators.cache import never_cache

import os

from rede.models import *
from rede.forms import *


class PlanoAdmin(ModelAdmin):
    list_display = ('nome','download','upload')
    class Meta:
        model = Plano
site.register(Plano, PlanoAdmin)


class PontoRedeAdmin(ModelAdmin):
    list_display = ('desc','ip','mac','plano','liberado','usa_proxy')
    list_filter = ('liberado','plano')
    search_fields = ['desc','ip','mac']
    form = PontoRedeForm
    actions = ['liberar','negar']

    class Meta:
        model = PontoRede


    def get_urls(self):
        """
        Sobrescreve o metodo get_urls adicionando novas urls mapeando
        views escritas dentro da classe PontoRedeAdmin.
        """

        from django.conf.urls.defaults import patterns
        urls = super(PontoRedeAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^firewall/$', self.admin_site.admin_view(self.run_firewall)),
            (r'^conectados/$', self.admin_site.admin_view(self.conectados)),
            (r'^conectados/cadastrar/$', self.admin_site.admin_view(self.cadastrar)),
            (r'^conectados/action/$', self.admin_site.admin_view(self.custom_action)),
        )
        return my_urls + urls

    def run_firewall(self, request):
        """
        Executa um shell script e exibe a mensagem retornada pelo script na tela.
        """

        if request.method == 'GET':
            executar = request.GET.get('executar')
            if not os.path.exists(settings.FIREWALL_SCRIPT):
                return HttpResponse('Script de Firewall nao localizado: %s' % settings.FIREWALL_SCRIPT)

            if executar == 'firewall':
                script = 'sudo %s start' % settings.FIREWALL_SCRIPT
            elif executar == 'stoptraffic':
                script = 'sudo %s stoptraffic' % settings.FIREWALL_SCRIPT
            else:
                script = ''
            try:
                resultado = os.popen(script)
                msg_retorno_script = resultado.readlines()[0]
            except:
                msg_retorno_script = 'Erro ao tentar exeuctar o script.'

            return direct_to_template(request,'retorno_firewall.html',extra_context={'msg': msg_retorno_script})
        else:
            return HttpResponse('Nao foi passado nenhum parametro via GET')


    def _montar_lista_conectados(self, lista_ip):
        """
        Retorna uma lista contendo o IP, MAC e outros dados do ponto de rede
        """
        conectados = []
        for item in lista_ip:
            linha = item.split()
            ip = linha[0]
            mac = linha[2]
            try:
                ponto = PontoRede.objects.get(ip=ip)
                dados_ponto = {
                    'id': ponto.id,
                    'desc': ponto.desc,
                    'ip': ponto.ip,
                    'mac': ponto.mac,
                    'cadastrado': True,
                    'liberado': ponto.liberado,
                    'usa_proxy': ponto.usa_proxy,
                    'plano': ponto.plano
                }
            except:
                dados_ponto = {
                    'id': 0,
                    'desc': u'Máquina não cadastrada',
                    'ip': ip,
                    'mac': mac,
                    'cadastrado': False,
                    'liberado': False,
                    'usa_proxy': True,
                    'plano': ''
                }
            conectados.append(dados_ponto)
        return conectados

    @never_cache
    def conectados(self, request):
        """
        Obtém a lista de IPs conectados e exibe na tela.
        """

        arp_exec = os.popen(settings.ARP_COMMAND)
        lista_ip = arp_exec.readlines()

        planos = Plano.objects.all()

        context = {
            'conectados': self._montar_lista_conectados(lista_ip), # IPs conectados
            'planos': planos,         # planos cadastrados
            'media': self.media       # includes javascript do admin
        }
        return direct_to_template(request,'conectados.html',extra_context=context)


    def _cadastrar_ponto_conectado(self, dados_ponto):
        """
        Cadastra um ponto de rede.
        Por padrão deixa o IP desliberado e usando proxy.
        """

        form = PontoRedeConectadoEnaoCadastradoForm(dados_ponto)
        if form.is_valid():
            try:
                form.save()
                status = 'ok'
            except:
                status = 'error'
        else:
            for item in form.errors:
                status = item

        return status


    def cadastrar(self, request):
        """
        Cadastra um ponto de rede.
        Por padrão deixa o IP desliberado e usando proxy.
        """

        if request.method == 'POST':
            resultado = self._cadastrar_ponto_conectado(request.POST)
            if resultado == 'ok':
                return HttpResponseRedirect('../')
            elif resultado == 'error':
                return HttpResponse('Dados insuficientes para cadatrar')
            else:
                return HttpResponse('Preencha corretamente o form')

        else:
            return HttpResponse('Nenhum formulario enviado via POST')


    def liberar(self, request, queryset):
        """
        Bloqueia os IPs selecionados.
        """

        queryset.update(liberado=True)
    liberar.short_description = 'liberar acesso'


    def negar(self, request, queryset):
        """
        Desbloqueia os IPs selecionados.
        """

        queryset.update(liberado=False)
    negar.short_description = 'negar acesso'


    def custom_action(self, request):
        """
        Executa um comando
        """

        if request.method == 'GET':
            acao = request.GET.get('acao')
            id = request.GET.getlist('id')
            try:
                pontorede = PontoRede.objects.filter(id__in=id)
                if acao == 'liberar':
                    pontorede.update(liberado=True)
                elif acao == 'negar':
                    pontorede.update(liberado=False)
                else:
                    return HttpResponse('nenhuma action definida.')
                return HttpResponseRedirect('../')
            except:
                pass
        else:
            return HttpResponse('Nenhum dado passado via GET.')


    def changelist_view(self, request, extra_context=None, **kwargs):
        """
        Sobrescreve o metodo changelist_view responsavel por exibir os dados do objeto,
        adicionando o total de IPs liberados e negados.
        Cria o arquivo texto usado pelos shell scripts de firewall e controle de banda.
        """

        from django.contrib.admin.views.main import ChangeList
        cl = ChangeList(request, self.model, list(self.list_display),
                        self.list_display_links, self.list_filter,
                        self.date_hierarchy, self.search_fields,
                        self.list_select_related,
                        self.list_per_page,
                        self.list_editable,
                        self)
        cl.formset = None

        if extra_context is None:
            extra_context = {}

        linha_arquivo_texto = ''
        total_liberados = 0
        pontos_de_rede = PontoRede.objects.all()
        for ponto in pontos_de_rede:
            if ponto.liberado:
                total_liberados += 1

            # ID - Desc - IP - MAC - Download - Upload - Liberado - Proxy
            linha_arquivo_texto += '%s-%s-%s-%s-%s-%s-%s-%s\n' % (ponto.id, ponto.desc.replace(' ','_'), ponto.ip, ponto.mac.upper(), ponto.plano.download, ponto.plano.upload, ponto.liberado, ponto.usa_proxy)

        # Calcula o total de IPs bloqueados
        total_negados = pontos_de_rede.count() - total_liberados

        # Salva o conteudo no arquivo texto
        arq = open(settings.FIREWALL_TXT_FILE, 'wb')
        arq.write(linha_arquivo_texto)
        arq.close()

        extra_context['cl'] = cl
        extra_context['total_liberados'] = total_liberados
        extra_context['total_negados'] = total_negados
        return super(PontoRedeAdmin, self).changelist_view(request, extra_context=extra_context)

site.register(PontoRede, PontoRedeAdmin)

