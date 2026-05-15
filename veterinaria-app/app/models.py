import datetime
from flask_appbuilder import Model
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship


class Dueno(Model):
    __tablename__ = "dueno"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)
    estado = Column(Boolean, nullable=True)
    creado_en = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    actualizado_en = Column(DateTime, default=datetime.datetime.utcnow,
                             onupdate=datetime.datetime.utcnow, nullable=False)

    mascotas = relationship("Mascota", back_populates="dueno")

    def __repr__(self):
        return self.nombre


class Mascota(Model):
    __tablename__ = "mascota"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    tipo = Column(String(50), nullable=False)
    edad = Column(Integer, nullable=True)

    dueno_id = Column(Integer, ForeignKey("dueno.id"), nullable=False)

    estado = Column(Boolean, nullable=True)
    creado_en = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    actualizado_en = Column(DateTime, default=datetime.datetime.utcnow,
                             onupdate=datetime.datetime.utcnow, nullable=False)

    dueno = relationship("Dueno", back_populates="mascotas")
    consultas = relationship("Consulta", back_populates="mascota")

    def __repr__(self):
        return self.nombre


class Veterinario(Model):
    __tablename__ = "veterinario"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    especialidad = Column(String(100), nullable=True)

    estado = Column(Boolean, nullable=True)
    creado_en = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    actualizado_en = Column(DateTime, default=datetime.datetime.utcnow,
                             onupdate=datetime.datetime.utcnow, nullable=False)

    consultas = relationship("Consulta", back_populates="veterinario")

    def __repr__(self):
        return self.nombre
class Consulta(Model):
    __tablename__ = "consulta"

    id = Column(Integer, primary_key=True)
    motivo = Column(Text, nullable=False)
    fecha = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    mascota_id = Column(Integer, ForeignKey("mascota.id"), nullable=False)
    veterinario_id = Column(Integer, ForeignKey("veterinario.id"), nullable=False)

    mascota = relationship("Mascota", back_populates="consultas")
    veterinario = relationship("Veterinario", back_populates="consultas")
    tratamientos = relationship("Tratamiento", back_populates="consulta")

    def __repr__(self):
        return f"Consulta {self.id}"


class Tratamiento(Model):
    __tablename__ = "tratamiento"

    id = Column(Integer, primary_key=True)
    descripcion = Column(Text, nullable=False)

    consulta_id = Column(Integer, ForeignKey("consulta.id"), nullable=False)

    consulta = relationship("Consulta", back_populates="tratamientos")

    def __repr__(self):
        return self.descripcion

    