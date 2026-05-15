from .extensions import appbuilder, db
from flask_appbuilder import BaseView, ModelView, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface

from .models import (
    Consulta,
    Dueno,
    Mascota,
    Tratamiento,
    Veterinario,
    Consulta,
    Tratamiento
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
class ConsultaModelView(ModelView):
    datamodel = SQLAInterface(Consulta)

    list_columns = ["mascota", "veterinario", "motivo", "fecha"]
    add_columns = ["mascota", "veterinario", "motivo"]
    edit_columns = ["mascota", "veterinario", "motivo"]
    show_columns = ["mascota", "veterinario", "motivo", "fecha"]


class TratamientoModelView(ModelView):
    datamodel = SQLAInterface(Tratamiento)

    list_columns = ["descripcion", "consulta"]
    add_columns = ["descripcion", "consulta"]
    edit_columns = ["descripcion", "consulta"]
    show_columns = ["descripcion", "consulta"]



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
appbuilder.add_view(
    ConsultaModelView,
    "Consultas",
    icon="fa-stethoscope",
    category="Consultas"
)

appbuilder.add_view(
    TratamientoModelView,
    "Tratamientos",
    icon="fa-medkit",
    category="Consultas"
)