const express    = require('express')
const mongoose   = require('mongoose')
const dotenv     = require('dotenv')
const cors       = require('cors')
const cajaRoutes = require('./routes/caja')

dotenv.config()

const app = express()
app.use(express.json())
app.use(cors())

mongoose.connect(process.env.MONGO_URI)
    .then(function() { console.log('MongoDB conectado — caja_db') })
    .catch(function(err) { console.error('Error MongoDB:', err) })

app.use('/api/caja', cajaRoutes)

var PORT = process.env.PORT || 8003
app.listen(PORT, function() {
    console.log('Microservicio Caja corriendo en puerto ' + PORT)
})