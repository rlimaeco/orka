#coding: utf-8

from flask.ext.appbuilder import ModelView
from flask.ext.appbuilder.models.sqla.interface import SQLAInterface
from app.models.image import Image
from container import ContainerModelView
from app import cli
import json

class ImageModelView(ModelView):
    datamodel = SQLAInterface(Image)

    related_views = [ContainerModelView]

    list_columns = ['name', 'version']

    base_order = ('name', 'asc')

    def pre_add(self, item):
        """
        Antes de criar o objeto no banco
        executa a criação da imagem
        :param item: objeto Image definido em models
        :return:
        """
        super(ImageModelView, self).pre_add(item)

        if item.name:
            if not item.version:
                item.version = "latest"

            image_raw = cli.pull("%s:%s" % (item.name, item.version))
            image_raw = image_raw.replace("\r\n","|")
            image_raw = image_raw.split("|")

            for raw in image_raw:
                try:
                    raw = json.loads(raw)
                    status = raw['status']

                    if status[:6] == "Digest":
                        item.digest = status[15:]
                except:
                    continue



    def pre_delete(self, item):
        """
        Antes de remover o imagem do banco
        mata o processo e remove
        :param item: objeto Image
        :return:
        """
        super(ImageModelView, self).pre_delete(item)

        if item.name:
            try:
                resp = cli.remove_image("%s:%s" % (item.name, item.version))
                if resp:
                    print resp
            except Exception as inst:
                if inst.response.status_code == 409:
                    #TODO: Perguntar se deseja remover o container associado
                    print "Necessita remover container associado a imagem"


