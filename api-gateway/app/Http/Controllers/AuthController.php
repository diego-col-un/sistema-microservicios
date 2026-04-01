<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;
use App\Models\User;

class AuthController extends Controller
{
    // ─────────────────────────────────────────
    // POST /api/auth/register
    // Registra usuario con pregunta y respuesta secreta
    // ─────────────────────────────────────────
    public function register(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'name'              => 'required|string|max:255',
            'email'             => 'required|string|email|unique:users',
            'password'          => 'required|string|min:6|confirmed',
            'security_question' => 'required|string|max:255',
            'security_answer'   => 'required|string|max:255',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'success' => false,
                'errors'  => $validator->errors()
            ], 422);
        }

        $user = User::create([
            'name'              => $request->name,
            'email'             => $request->email,
            'password'          => Hash::make($request->password),
            'security_question' => $request->security_question,
            'security_answer'   => Hash::make(strtolower(trim($request->security_answer))),
        ]);

        return response()->json([
            'success' => true,
            'message' => 'Usuario registrado correctamente',
            'user'    => $user
        ], 201);
    }

    // ─────────────────────────────────────────
    // POST /api/auth/login
    // ─────────────────────────────────────────
    public function login(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'email'    => 'required|email',
            'password' => 'required|string',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'success' => false,
                'errors'  => $validator->errors()
            ], 422);
        }

        $user = User::where('email', $request->email)->first();

        if (!$user || !Hash::check($request->password, $user->password)) {
            return response()->json([
                'success' => false,
                'message' => 'Credenciales incorrectas'
            ], 401);
        }

        // ← Quitamos $user->tokens()->delete() para permitir múltiples sesiones
        $token = $user->createToken('auth_token')->plainTextToken;

        return response()->json([
            'success' => true,
            'message' => 'Login exitoso',
            'token'   => $token,
            'user'    => $user
        ], 200);
    }

    // ─────────────────────────────────────────
    // POST /api/auth/logout
    // Revoca el token actual
    // ─────────────────────────────────────────
    public function logout(Request $request)
    {
        try {
            $request->user()->currentAccessToken()->delete();
            return response()->json([
                'success' => true,
                'message' => 'Sesión cerrada correctamente'
            ], 200);
        } catch (\Throwable $e) {
            return response()->json([
                'success' => false,
                'message' => $e->getMessage(),
                'line'    => $e->getLine(),
                'file'    => $e->getFile()
            ], 500);
        }
    }

    // ─────────────────────────────────────────
    // GET /api/auth/me
    // Devuelve el usuario autenticado
    // ─────────────────────────────────────────
    public function me(Request $request)
    {
        return response()->json([
            'success' => true,
            'user'    => $request->user()
        ], 200);
    }

    // ─────────────────────────────────────────
    // POST /api/auth/obtener-pregunta
    // PASO 1 del reset — devuelve la pregunta secreta
    // ─────────────────────────────────────────
    public function obtenerPregunta(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'email' => 'required|email|exists:users,email',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'success' => false,
                'errors'  => $validator->errors()
            ], 422);
        }

        $user = User::where('email', $request->email)->first();

        return response()->json([
            'success'           => true,
            'security_question' => $user->security_question
        ], 200);
    }

    // ─────────────────────────────────────────
    // POST /api/auth/reset-password
    // PASO 2 del reset — verifica respuesta y cambia password
    // ─────────────────────────────────────────
    public function resetPassword(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'email'           => 'required|email|exists:users,email',
            'security_answer' => 'required|string',
            'password'        => 'required|string|min:6|confirmed',
        ]);

        if ($validator->fails()) {
            return response()->json([
                'success' => false,
                'errors'  => $validator->errors()
            ], 422);
        }

        $user = User::where('email', $request->email)->first();

        if (!Hash::check(strtolower(trim($request->security_answer)), $user->security_answer)) {
            return response()->json([
                'success' => false,
                'message' => 'Respuesta secreta incorrecta'
            ], 401);
        }

        $user->update([
            'password' => Hash::make($request->password)
        ]);

        $user->tokens()->delete();

        return response()->json([
            'success' => true,
            'message' => 'Contraseña actualizada correctamente. Inicia sesión de nuevo.'
        ], 200);
    }
}