import requests
from django.conf import settings

## Funciones para los endpoints de CertsGen

def register_accreditation_authority(owner, name, id, password, email):
    payload = {
        'owner': owner,
        'name': name,
        'id': id,
        'password': password,
        'email': email }
    url = f"{settings.CERTSGEN_URL}/api/register/accreditation-authority/"
    headers = {}
    response = requests.post(url, json=payload, headers=headers)
    return response


def auth_accreditation_authority(username, password):
    payload = {
        'password': password,
        'username': username }
    url = f"{settings.CERTSGEN_URL}/api/auth/accreditation-authority/"
    headers = {}
    response = requests.post(url, json=payload, headers=headers)
    return response


def register_certification_authority(token, owner, name, id, email):
    headers = { "Authorization": "Token {}".format(token)}
    payload = {
        	'owner': owner,
        	'name': name,
        	'id': id,
        	'email': email,
    }
    url = f"{settings.CERTSGEN_URL}/api/register/certification-authority/"
    response = requests.post(url, data=payload, headers=headers)
    return response


def register_certifier(token, owner, name, id_number, id, email):
    headers = { "Authorization": "Token {}".format(token)}
    payload = {
        	'owner': owner,
        	'name': name,
        	'id_number': id_number,
            'id': id,
        	'email': email,
    }
    url = f"{settings.CERTSGEN_URL}/api/register/certifier/"
    response = requests.post(url, data=payload, headers=headers)
    return response


def register_recipient(token, owner, first_name, last_name, id, id_number, email):
    headers = { "Authorization": "Token {}".format(token)}
    payload = {
            'owner': owner,
            'name': '%s' %first_name+' '+last_name,
            'id': id,
            'id_number':1000+id_number,
            'email': email}
    url = f"{settings.CERTSGEN_URL}/api/register/recipient/"
    response = requests.post(url, json=payload, headers=headers)


def register_certificate(token, recipient_address, titulo, descripcion):
    headers = { "Authorization": "Token {}".format(token)}
    payload = {
        'recipient_address': recipient_address,
        'title': titulo,
        'description': descripcion
    }
    url = f"{settings.CERTSGEN_URL}/api/register/certificate/"
    response = requests.post(url, json=payload, headers=headers)
    return response


def add_signature(token, certificate_address, first_name, last_name):
    headers = { "Authorization": "Token {}".format(token)}
    payload = {
        'certificate_address': certificate_address,
        'params': f'P.A. {first_name} {last_name}'
    }
    url = f"{settings.CERTSGEN_URL}/api/add/signature/"
    response = requests.post(url, json=payload, headers=headers)


def add_denpendency(token, certificate_address, from_owner, to_owner):
    headers = { "Authorization": "Token {}".format(token)}
    payload = {
                'certificate_address': certificate_address,
                'from_owner': from_owner,
                'to_owner': to_owner
    }
    url = f"{settings.CERTSGEN_URL}/api/add/certifier-dependency/"
    response = requests.post(url, json=payload, headers=headers)


def get_certificates(token):
    headers = { "Authorization": "Token {}".format(token)}
    url = f"{settings.CERTSGEN_URL}/api/get/certificates/"
    response = requests.get(url, headers=headers)
    return response