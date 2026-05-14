from .extensions import appbuilder, db
from flask_appbuilder import BaseView, ModelView, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface

from .models import (
    Dueno,
    Mascota,
    Veterinario,
#    Consulta,
#    Tratamiento
)


class DuenoModelView(ModelView):
    datamodel = SQLAInterface(Dueno)

    list_columns = ["nombre", "telefono", "estado"]
    add_columns = ["nombre", "telefono", "estado"]
    edit_columns = ["nombre", "telefono", "estado"]
    show_columns = ["nombre", "telefono", "estado", "creado_en"]


class MascotaModelView(ModelView):
    datamodel = SQLAInterface(Mascota)

    list_columns = ["nombre", "tipo", "edad", "dueno", "estado"]
    add_columns = ["nombre", "tipo", "edad", "dueno", "estado"]
    edit_columns = ["nombre", "tipo", "edad", "dueno", "estado"]
    show_columns = ["nombre", "tipo", "edad", "dueno", "estado", "creado_en"]


class VeterinarioModelView(ModelView):
    datamodel = SQLAInterface(Veterinario)

    list_columns = ["nombre", "especialidad", "estado"]
    add_columns = ["nombre", "especialidad", "estado"]
    edit_columns = ["nombre", "especialidad", "estado"]
    show_columns = ["nombre", "especialidad", "estado", "creado_en"]
#1

#2



appbuilder.add_view(
    DuenoModelView,
    "Dueños",
    icon="fa-user",
    category="Veterinaria"
)

appbuilder.add_view(
    MascotaModelView,
    "Mascotas",
    icon="fa-paw",
    category="Veterinaria"
)

appbuilder.add_view(
    VeterinarioModelView,
    "Veterinarios",
    icon="fa-user-md",
    category="Veterinaria"
)
#1


#2
