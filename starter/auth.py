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
    if len(header_parts) < 2 or header_parts[0] != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Header malformed'
        }, 401)
    
    # RETURN TOKEN PART
    return auth_header[1]

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

# 3. CHECK PERMISSION USE PAYLOAD FROM TOKEN
def check_permissions(permission, payload):
    if 'permission' not in payload:
        raise AuthError({
            'code': 'permission_error',
            'description': 'Permission not presented in payload'
        }, 401)
    
    if permission not in payload['permission']:
        raise AuthError({
            'code': 'permission_error',
            'description': 'Request permission is not authorized'
        }, 403)

# 4. 