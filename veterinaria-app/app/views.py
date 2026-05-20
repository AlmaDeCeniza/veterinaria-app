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
    TipoMascota,
    Consulta,
    Tratamiento
)
from .ia_servicio import analizar_recurrencia

from .models import (
    Consulta,
    Dueno,
    Mascota,
    Tratamiento,
    Veterinario,
    TipoMascota,
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
    label_columns = {"foto_preview": "Foto", "dueno": "Dueño", "tipo": "Especie"}
    list_columns = ["nombre", "tipo", "edad", "dueno", "estado", "foto_preview"]
    add_columns = ["nombre", "tipo", "edad", "dueno", "estado", "imagen_file"]
    edit_columns = ["nombre", "tipo", "edad", "dueno", "estado","imagen_file"]
    show_columns = ["nombre", "tipo", "edad", "dueno", "estado", "foto_preview","creado_en"]
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

class TipoMascotaModelView(ModelView):
    datamodel = SQLAInterface(TipoMascota)
    list_columns = ["nombre"]
    add_columns = ["nombre"]
    edit_columns = ["nombre"]
    show_columns = ["nombre"]
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

class PacientesReporteView(BaseView):
    route_base = '/reporte-pacientes'

    @expose('/')
    def index(self):
        total_pacientes = db.session.query(Mascota).count()

        distribucion_especies = db.session.query(
            TipoMascota.nombre,
            db.func.count(Mascota.id)
        ).join(Mascota).group_by(TipoMascota.nombre).all()

        edad_promedio = db.session.query(db.func.avg(Mascota.edad)).scalar()
        edad_promedio = round(edad_promedio, 1) if edad_promedio else 0

        return self.render_template(
            'reportes_pacientes.html',
            total_pacientes=total_pacientes,
            distribucion_especies=distribucion_especies,
            edad_promedio=edad_promedio
        )

class TemporalReporteView(BaseView):
    route_base = '/reporte-temporal'

    @expose('/')
    def index(self):
        # Obtener fechas del filtro desde la request
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')

        query = db.session.query(Consulta.fecha)

        # Aplicar filtros si existen
        if start_date_str:
            try:
                from datetime import datetime
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                query = query.filter(Consulta.fecha >= start_date)
            except ValueError:
                pass

        if end_date_str:
            try:
                from datetime import datetime
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                query = query.filter(Consulta.fecha <= end_date)
            except ValueError:
                pass

        consultas = query.all()

        # Diccionario para contar consultas por mes (formato 'YYYY-MM')
        conteo_mensual = {}

        for c in consultas:
            fecha = c.fecha
            if fecha:
                mes_clave = fecha.strftime('%Y-%m')
                conteo_mensual[mes_clave] = conteo_mensual.get(mes_clave, 0) + 1

        # Ordenar los meses cronológicamente
        labels = sorted(conteo_mensual.keys())
        data = [conteo_mensual[mes] for mes in labels]

        return self.render_template(
            'reportes_temporal.html',
            labels=labels,
            data=data,
            start_date=start_date_str,
            end_date=end_date_str
        )

class RecurrenciaPacientesReporteView(BaseView):
    route_base = '/reporte-recurrencia'

    @expose('/')
    def index(self):
        # Obtener mascotas con el conteo de sus consultas, ordenadas por las más frecuentes
        resultados = db.session.query(
            Mascota.nombre,
            TipoMascota.nombre,
            db.func.count(Consulta.id)
        ).join(Consulta).join(TipoMascota).group_by(Mascota.id, TipoMascota.nombre).order_by(db.func.count(Consulta.id).desc()).all()

        # Obtener análisis de la IA
        analisis_ia = analizar_recurrencia(resultados)

        return self.render_template(
            'reportes_recurrencia.html',
            resultados=resultados,
            analisis_ia=analisis_ia
        )

class EspeciesConsultasReporteView(BaseView):
    route_base = '/reporte-especies-consultas'

    @expose('/')
    def index(self):
        # Contar consultas agrupadas por el nombre del tipo de mascota
        # Empezamos la consulta desde Consulta para evitar errores de join
        resultados = db.session.query(
            TipoMascota.nombre,
            db.func.count(Consulta.id)
        ).select_from(Consulta).join(Mascota).join(TipoMascota).group_by(TipoMascota.nombre).all()

        total_consultas = sum(item[1] for item in resultados)

        return self.render_template(
            'reportes_especies_consultas.html',
            resultados=resultados,
            total_consultas=total_consultas
        )


appbuilder.add_view(
    DuenoModelView,
    "Dueños",
    icon="fa-user",
    category="Administración"
)

appbuilder.add_view(
    MascotaModelView,
    "Mascotas",
    icon="fa-paw",
    category="Administración"
)

appbuilder.add_view(
    TipoMascotaModelView,
    "Tipos de Mascota",
    icon="fa-list",
    category="Administración"
)

appbuilder.add_view(
    VeterinarioModelView,
    "Veterinarios",
    icon="fa-user-md",
    category="Administración"
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
appbuilder.add_view_no_menu(PacientesReporteView())
appbuilder.add_view_no_menu(TemporalReporteView())
appbuilder.add_view_no_menu(EspeciesConsultasReporteView())
appbuilder.add_view_no_menu(RecurrenciaPacientesReporteView())

appbuilder.add_link(
    "Consultas por Veterinario",
    href="/reportes/",
    icon="fa-bar-chart",
    category="Reportes"
)

appbuilder.add_link(
    "Recurrencia de Pacientes",
    href="/reporte-recurrencia/",
    icon="fa-redo",
    category="Reportes"
)

appbuilder.add_link(
    "Tendencia de Consultas",
    href="/reporte-temporal/",
    icon="fa-chart-line",
    category="Reportes"
)

appbuilder.add_link(
    "Consultas por Especie",
    href="/reporte-especies-consultas/",
    icon="fa-dog",
    category="Reportes"
)

appbuilder.add_link(
    "Análisis de Pacientes",
    href="/reporte-pacientes/",
    icon="fa-paw",
    category="Reportes"
)
