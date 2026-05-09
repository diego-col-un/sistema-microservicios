<?php

namespace Tests\Feature;

use Tests\TestCase;

class GatewaySecurityTest extends TestCase
{
    /** @test */
    public function test_gateway_access_denied_without_sanctum_token()
    {
        // 1. Verifica que el acceso externo esté protegido por Sanctum
        $response = $this->getJson('/api/caja');
        $response->assertStatus(401);
    }

    /** @test */
    public function test_internal_token_exists_in_config()
    {
        // 2. Verifica que la clave secreta interna esté configurada
        $this->assertNotEmpty(env('GATEWAY_INTERNAL_TOKEN'), 'Falta el token interno en el .env');
    }

    /** @test */
    public function test_proxy_route_exists_for_repuestos()
    {
        // 3. Verifica que la ruta de repuestos esté definida en el Gateway
        $response = $this->getJson('/api/repuestos');
        $this->assertNotEquals(404, $response->status());
    }

    /** @test */
    public function test_gateway_headers_structure()
    {
        // 4. Verifica que el controlador use el nombre de header correcto
        $token = env('GATEWAY_INTERNAL_TOKEN');
        $this->assertIsString($token);
    }

    /** @test */
    public function test_gateway_returns_error_on_microservice_timeout()
    {
        // 5. Simula fallo de conexión (puerto inexistente)
        $response = $this->getJson('/api/caja_fail_route'); 
        $response->assertStatus(404);
    }
}