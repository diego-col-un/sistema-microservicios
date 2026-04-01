const mongoose = require('mongoose')

const transaccionSchema = new mongoose.Schema({
    tipo:        { type: String, enum: ['ingreso', 'egreso'], required: true },
    categoria:   { type: String, enum: ['venta_taller', 'venta_restaurante', 'gasto', 'otro'], required: true },
    descripcion: { type: String, required: true },
    monto:       { type: Number, required: true },
    usuario_id:  { type: String, required: true },
    referencia_id: { type: String },
    fecha:       { type: Date, default: Date.now }
})

module.exports = mongoose.model('Transaccion', transaccionSchema)