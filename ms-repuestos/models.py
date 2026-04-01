from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Repuesto(db.Model):
    __tablename__ = 'repuestos'

    id          = db.Column(db.Integer, primary_key=True)
    nombre      = db.Column(db.String(200), nullable=False)
    referencia  = db.Column(db.String(100), unique=True, nullable=False)
    marca       = db.Column(db.String(100), nullable=False)
    precio      = db.Column(db.Float, nullable=False)
    stock       = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=5)
    descripcion = db.Column(db.Text, nullable=True)
    created_at  = db.Column(db.DateTime, server_default=db.func.now())
    updated_at  = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        return {
            'id':           self.id,
            'nombre':       self.nombre,
            'referencia':   self.referencia,
            'marca':        self.marca,
            'precio':       self.precio,
            'stock':        self.stock,
            'stock_minimo': self.stock_minimo,
            'descripcion':  self.descripcion,
            'created_at':   str(self.created_at),
            'updated_at':   str(self.updated_at)
        }