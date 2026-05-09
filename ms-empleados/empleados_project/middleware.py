from django.http import HttpResponseForbidden

class GatewayOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Token que debe coincidir con el de Laravel
        token_esperado = "mi_token_secreto_123" 
        token_recibido = request.headers.get('X-Gateway-Secret')

        if token_recibido != token_esperado:
            return HttpResponseForbidden("Acceso denegado: Debe pasar por el API Gateway.")

        return self.get_response(request)