const request = require('supertest');
const expect = require('chai').expect;
const app = require('../index'); // Asegúrate de que index.js haga: module.exports = app;

describe('Tests Unitarios: Microservicio Caja', () => {
    
    // Test 6
    it('Debe retornar 403 si el header X-Gateway-Secret no está presente', (done) => {
        request(app)
            .get('/api/caja')
            .end((err, res) => {
                expect(res.status).to.equal(403);
                expect(res.body.success).to.be.false;
                done();
            });
    });

    // Test 7
    it('Debe retornar 403 si el token es incorrecto', (done) => {
        request(app)
            .get('/api/caja')
            .set('x-gateway-secret', 'token_falso_123')
            .end((err, res) => {
                expect(res.status).to.equal(403);
                done();
            });
    });

    // Test 8
    it('Debe cargar correctamente las variables de entorno (.env)', () => {
        expect(process.env.GATEWAY_INTERNAL_TOKEN).to.not.be.undefined;
    });

    // Test 9
    it('La respuesta de la DB debe ser un objeto JSON', (done) => {
        request(app)
            .get('/api/caja')
            .set('x-gateway-secret', process.env.GATEWAY_INTERNAL_TOKEN)
            .end((err, res) => {
                // Si el token es correcto, no debería ser 403
                expect(res.status).to.not.equal(403);
                expect(res.headers['content-type']).to.match(/json/);
                done();
            });
    });
});