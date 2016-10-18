#coding: utf-8
from flask import jsonify
from flask.ext.appbuilder import IndexView, has_access, expose
from flask import g, redirect, url_for, request, redirect, make_response, session
from models.service import Service
from models.container import Container
from models.node import Node

class IndexView(IndexView):
    index_template = 'index.html'

    @expose('/')
    @has_access
    def index(self):
        containers = self.appbuilder.session.query(Container).filter_by(created_by=g.user).all()
        services = self.appbuilder.session.query(Service).filter_by(created_by=g.user).all()
        nodes = self.appbuilder.session.query(Node).all()
        self.update_redirect()

        return self.render_template(self.index_template,
                                    appbuilder=self.appbuilder,
                                    containers=containers,
                                    services=services,
                                    nodes=nodes
                                    )

    # TODO: Informações do sistema para o json, requisição se repete a cada 2,5 segundos no FrontEnd##
    @expose('/usage', methods=['GET'])
    @has_access
    def usage(self):
        dados_dict = {'chave': 'diogao, envio oq aqui pra vc ?'}
        return jsonify(dados_dict)

