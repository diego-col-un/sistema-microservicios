const express      = require('express')
const router       = express.Router()
const Transaccion  = require('../models/transaccion')

// ─────────────────────────────────────────
// GET /api/caja — listar todas
// ─────────────────────────────────────────
router.get('/', function(req, res) {
    Transaccion.find().sort({ fecha: -1 })
        .then(function(transacciones) {
            res.json({ success: true, data: transacciones })
        })
        .catch(function(err) {
            res.status(500).json({ success: false, message: err.message })
        })
})

// ─────────────────────────────────────────
// GET /api/caja/:id — obtener una
// ─────────────────────────────────────────
router.get('/:id', function(req, res) {
    Transaccion.findById(req.params.id)
        .then(function(transaccion) {
            if (!transaccion) {
                return res.status(404).json({ success: false, message: 'Transacción no encontrada' })
            }
            res.json({ success: true, data: transaccion })
        })
        .catch(function(err) {
            res.status(500).json({ success: false, message: err.message })
        })
})

// ─────────────────────────────────────────
// POST /api/caja — registrar transaccion
// ─────────────────────────────────────────
router.post('/', function(req, res) {
    var tipo        = req.body.tipo
    var categoria   = req.body.categoria
    var descripcion = req.body.descripcion
    var monto       = req.body.monto
    var usuario_id  = req.body.usuario_id

    if (!tipo || !categoria || !descripcion || !monto || !usuario_id) {
        return res.status(400).json({
            success: false,
            message: 'tipo, categoria, descripcion, monto y usuario_id son requeridos'
        })
    }

    var transaccion = new Transaccion({
        tipo,
        categoria,
        descripcion,
        monto,
        usuario_id,
        referencia_id: req.body.referencia_id
    })

    transaccion.save()
        .then(function(t) {
            res.status(201).json({ success: true, data: t })
        })
        .catch(function(err) {
            res.status(500).json({ success: false, message: err.message })
        })
})

// ─────────────────────────────────────────
// GET /api/caja/resumen/:fecha — resumen del dia
// ─────────────────────────────────────────
router.get('/resumen/:fecha', function(req, res) {
    var inicio = new Date(req.params.fecha)
    var fin    = new Date(req.params.fecha)
    fin.setDate(fin.getDate() + 1)

    Transaccion.find({ fecha: { $gte: inicio, $lt: fin } })
        .then(function(transacciones) {
            var ingresos = transacciones
                .filter(function(t) { return t.tipo === 'ingreso' })
                .reduce(function(sum, t) { return sum + t.monto }, 0)

            var egresos = transacciones
                .filter(function(t) { return t.tipo === 'egreso' })
                .reduce(function(sum, t) { return sum + t.monto }, 0)

            res.json({
                success: true,
                data: {
                    fecha:        req.params.fecha,
                    ingresos:     ingresos,
                    egresos:      egresos,
                    balance:      ingresos - egresos,
                    transacciones: transacciones
                }
            })
        })
        .catch(function(err) {
            res.status(500).json({ success: false, message: err.message })
        })
})

// ─────────────────────────────────────────
// POST /api/caja/cierre — cierre de caja
// ─────────────────────────────────────────
router.post('/cierre', function(req, res) {
    var hoy   = new Date()
    var inicio = new Date(hoy.getFullYear(), hoy.getMonth(), hoy.getDate())
    var fin    = new Date(hoy.getFullYear(), hoy.getMonth(), hoy.getDate() + 1)

    Transaccion.find({ fecha: { $gte: inicio, $lt: fin } })
        .then(function(transacciones) {
            var ingresos = transacciones
                .filter(function(t) { return t.tipo === 'ingreso' })
                .reduce(function(sum, t) { return sum + t.monto }, 0)

            var egresos = transacciones
                .filter(function(t) { return t.tipo === 'egreso' })
                .reduce(function(sum, t) { return sum + t.monto }, 0)

            res.json({
                success:  true,
                message:  'Cierre de caja realizado',
                data: {
                    fecha:    hoy.toISOString().split('T')[0],
                    ingresos: ingresos,
                    egresos:  egresos,
                    balance:  ingresos - egresos,
                    total_transacciones: transacciones.length
                }
            })
        })
        .catch(function(err) {
            res.status(500).json({ success: false, message: err.message })
        })
})

// ─────────────────────────────────────────
// DELETE /api/caja/:id — eliminar
// ─────────────────────────────────────────
router.delete('/:id', function(req, res) {
    Transaccion.findByIdAndDelete(req.params.id)
        .then(function(transaccion) {
            if (!transaccion) {
                return res.status(404).json({ success: false, message: 'Transacción no encontrada' })
            }
            res.json({ success: true, message: 'Transacción eliminada' })
        })
        .catch(function(err) {
            res.status(500).json({ success: false, message: err.message })
        })
})

module.exports = router