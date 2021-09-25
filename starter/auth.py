import json
from flask import request
from jose import jwt
from urllib.request import urlopen
from functools import wraps

# AUTH DOMAIN AND API AUDIENCE SETUP
AUTH0_DOMAIN = 'fsndantony.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'udacitycapstone'

# AUTH ERROR CUSTOM EXCEPTION
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# 1. GET TOKEN FROM AUTH HEADER
def get_token_auth_header():
    # CHECK AUTHORIZATION PRESENTED IN HEADERS
    if 'Authorization' not in request.headers:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization not presented in header'
        }, 401)
    auth_header = request.headers['Authorization']

    # CHECK TOKEN FORMAT
    header_parts = auth_header.split(' ')
    # print(header_parts)
    if len(header_parts) < 2 or header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Header malformed'
        }, 401)
    
    # RETURN TOKEN PART
    return header_parts[1]

# 2. VERIFY JWT
def verify_decode_jwt(token):
    # GET PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # GET DATA INSIDE HEADER
    unverified_token = jwt.get_unverified_header(token)

    # CHOOSE THE KEY
    rsa_key = {},
    if 'kid' not in unverified_token:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed'
        }, 401)
    
    for key in jwks['keys']:
        if key['kid'] == unverified_token['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
        
        if rsa_key:
            try:
                # USE THE KEY TO VERIFY JWT
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer=f'https://{AUTH0_DOMAIN}/'
                )
                return payload

            except jwt.ExpiredSignatureError:
                raise AuthError({
                    'code': 'token_expired',
                    'description': 'Token expired'
                }, 401)
            
            except jwt.JWTClaimsError:
                raise AuthError({
                    'code': 'invalid_claims',
                    'description': 'Incorrect claims. Please check the audience and issuer'
                }, 401)
            
            except Exception:
                raise AuthError({
                    'code': 'invalid_header',
                    'description': 'Unable to parse authentication token'
                }, 400)
        
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to find appropriate key.'
        }, 400)

# 3. CHECK PERMISSION USE PAYLOAD FROM TOKEN
def check_permissions(permission, payload):
    # print(permission)
    # print(payload)
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'permission_error',
            'description': 'Permission not presented in payload'
        }, 401)
    
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'permission_error',
            'description': 'Request permission is not authorized'
        }, 403)

# 4. Wrap it up as decorator
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        
        return wrapper
    return requires_auth_decorator