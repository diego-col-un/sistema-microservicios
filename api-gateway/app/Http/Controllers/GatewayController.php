<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class GatewayController extends Controller
{
    // ─────────────────────────────────────────
    // Proxy genérico — redirige al microservicio
    // ─────────────────────────────────────────
    private function proxy(Request $request, string $baseUrl, string $path)
    {
        try {
            $url = rtrim($baseUrl, '/') . '/' . ltrim($path, '/');
            $token = env('GATEWAY_INTERNAL_TOKEN', 'mi_token_secreto_123');

            // Usamos Http::withHeaders y pasamos los datos directamente
            $response = Http::timeout(10)
                ->withHeaders([
                    'X-Gateway-Secret' => $token,
                    'Accept'           => 'application/json',
                ])
                ->{strtolower($request->method())}($url, $request->all());

            return response()->json($response->json(), $response->status());
        } catch (\Exception $e) {
            return response()->json([
                'success' => false,
                'message' => 'Error al conectar con el microservicio: ' . $e->getMessage()
            ], 500);
        }
    }

    // ─────────────────────────────────────────
    // Reservas — Django :8001
    // ─────────────────────────────────────────
    public function reservas(Request $request, $path = '')
    {
        return $this->proxy($request, env('MS_RESERVAS_URL'), '/api/reservas/' . $path);
    }

    // ─────────────────────────────────────────
    // Repuestos — Flask :8002
    // ─────────────────────────────────────────
    public function repuestos(Request $request, $path = '')
    {
        return $this->proxy($request, env('MS_REPUESTOS_URL'), '/api/repuestos/' . $path);
    }

    // ─────────────────────────────────────────
    // Caja — Express :8003
    // ─────────────────────────────────────────
    public function caja(Request $request, $path = '')
    {
        return $this->proxy($request, env('MS_CAJA_URL'), '/api/caja/' . $path);
    }

    // ─────────────────────────────────────────
    // Menú restaurante — Flask :8004
    // ─────────────────────────────────────────
    public function menu(Request $request, $path = '')
    {
        return $this->proxy($request, env('MS_MENU_URL'), '/api/menu/' . $path);
    }

    // ─────────────────────────────────────────
    // Empleados — Django :8005
    // ─────────────────────────────────────────
    public function empleados(Request $request, $path = '')
    {
        return $this->proxy($request, env('MS_EMPLEADOS_URL'), '/api/empleados/' . $path);
    }
}