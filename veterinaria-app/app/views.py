import os
      
from werkzeug.utils import secure_filename
from wtforms import FileField
from flask import current_app, request
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
    add_form_extra_fields = {
    "imagen_file": FileField("Foto")
    }
    edit_form_extra_fields = {
        "imagen_file": FileField("Foto")
    }
    label_columns = {"foto_preview": "Foto", "dueno": "Dueño"}   
    list_columns = ["nombre", "tipo", "edad", "dueno", "estado", "foto_preview"]
    add_columns = ["nombre", "tipo", "edad", "dueno", "estado", "imagen_file"]
    edit_columns = ["nombre", "tipo", "edad", "dueno", "estado","imagen_file"]
    show_columns = ["nombre", "tipo", "edad", "dueno", "estado", "creado_en"]
    def pre_add(self, item):

        file = request.files.get("imagen_file")

        if file:

            filename = secure_filename(file.filename)

            upload_path = os.path.join(
                current_app.root_path,
                "static",
                "uploads"
            )

            os.makedirs(upload_path, exist_ok=True)

            file_path = os.path.join(upload_path, filename)

            file.save(file_path)

            item.foto = f"uploads/{filename}"
    def pre_update(self, item):
        
        file = request.files.get("imagen_file")

        if file and file.filename:

            filename = secure_filename(file.filename)

            upload_path = os.path.join(
                current_app.root_path,
                "static",
                "uploads"
            )

            os.makedirs(upload_path, exist_ok=True)

            file_path = os.path.join(upload_path, filename)

            file.save(file_path)

            item.foto = f"uploads/{filename}"
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
    
class ReporteView(BaseView):
    route_base = '/reportes'

    @expose('/')
    def index(self):

        total_consultas = db.session.query(Consulta).count()

        consultas_por_veterinario = db.session.query(
            Veterinario.nombre,
            db.func.count(Consulta.id)
        ).join(Consulta).group_by(Veterinario.nombre).all()

        return self.render_template(
            'reportes.html',
            total_consultas=total_consultas,
            consultas_por_veterinario=consultas_por_veterinario
        )


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
appbuilder.add_view_no_menu(ReporteView())

appbuilder.add_link(
    "Reporte",
    href="/reportes/",
    icon="fa-bar-chart",
    category="Reportes"
)