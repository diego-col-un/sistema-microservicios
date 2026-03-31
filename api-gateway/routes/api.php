<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\GatewayController;

// ─────────────────────────────────────────
// Rutas públicas — Sin autenticación
// ─────────────────────────────────────────
Route::prefix('auth')->group(function () {
    Route::post('/register',          [AuthController::class, 'register']);
    Route::post('/login',             [AuthController::class, 'login']);
    Route::post('/obtener-pregunta',  [AuthController::class, 'obtenerPregunta']);
    Route::post('/reset-password',    [AuthController::class, 'resetPassword']);
});

// ─────────────────────────────────────────
// Rutas protegidas — Requieren token Sanctum
// ─────────────────────────────────────────
Route::middleware('auth:sanctum')->group(function () {

    // Auth
    Route::post('/auth/logout', [AuthController::class, 'logout']);
    Route::get('/auth/me',      [AuthController::class, 'me']);

    // Microservicio Reservas (Django :8001)
    Route::any('/reservas/{path?}', [GatewayController::class, 'reservas'])
        ->where('path', '.*');

    // Microservicio Repuestos (Flask :8002)
    Route::any('/repuestos/{path?}', [GatewayController::class, 'repuestos'])
        ->where('path', '.*');

    // Microservicio Caja (Express :8003)
    Route::any('/caja/{path?}', [GatewayController::class, 'caja'])
        ->where('path', '.*');

    // Microservicio Menú (Flask :8004)
    Route::any('/menu/{path?}', [GatewayController::class, 'menu'])
        ->where('path', '.*');

    // Microservicio Empleados (Django :8005)
    Route::any('/empleados/{path?}', [GatewayController::class, 'empleados'])
        ->where('path', '.*');
});