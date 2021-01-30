from unittest.mock import Mock, patch
import pytest
from django.conf import settings
from apps.CertsGen import *


@pytest.mark.integration
@patch("apps.CertsGen.requests")
def test_register_accreditation_authority(mock_requests):
    owner = "0xeA88D2c82950a0D539438a53387a617327a8e1a3"
    name = "Autoridad Acreditacion"
    id = 1234
    password = "rewq4321"
    email = "ac.mppes1@gmail.com"
    register_accreditation_authority(owner, name, id, password, email)
    headers = {}
    payload = {
        'owner': owner,
        'name': name,
        'id': id,
        'password': password,
        'email': email }
    url = f"{settings.CERTSGEN_URL}/api/register/accreditation-authority/"
    mock_requests.post.assert_called_once_with(url, json=payload, headers=headers)


@pytest.mark.integration
@patch("apps.CertsGen.requests")
def test_auth_accreditation_authority(mock_requests):
    username = "autoridad-acreditacion"
    password = "4321rewq"
    auth_accreditation_authority(username, password)
    headers = {}
    payload = {
        'username': username,
        'password': password }
    url = f"{settings.CERTSGEN_URL}/api/auth/accreditation-authority/"
    mock_requests.post.assert_called_once_with(url, json=payload, headers=headers)
    

@pytest.mark.integration
@patch("apps.CertsGen.requests")
def test_register_certification_authority(mock_requests):
    token = "wkrmspr131refal2345"
    owner = "0x2870Db5e8230A861fBDe67d73d946f11D3E441f0"
    name = "Autoridad Certificacion"
    id = 5678
    email = "nataliocgre@gmail.com"
    register_certification_authority(token, owner, name, id, email)
    headers = { "Authorization": "Token {}".format(token)}
    payload = {
        	'owner': owner,
        	'name': name,
        	'id': id,
        	'email': email,
    }
    url = f"{settings.CERTSGEN_URL}/api/register/certification-authority/"
    mock_requests.post.assert_called_once_with(url, data=payload, headers=headers)


@pytest.mark.integration
@patch("apps.CertsGen.requests")
def test_register_certifier(mock_requests):
    token = "wkrmspr131refal2345"
    owner = "0x7BaA7C3294EDF61b054e47cfA96e8a5dF4144b73"
    name = "Certificador"
    id_number = "V-10867594"
    id = 5678
    email = "jm.ocgre@gmail.com"
    register_certifier(token, owner, name, id_number, id, email)
    headers = { "Authorization": "Token {}".format(token)}
    payload = {
        	'owner': owner,
        	'name': name,
            'id_number': id_number,
        	'id': id,
        	'email': email,
    }
    url = f"{settings.CERTSGEN_URL}/api/register/certifier/"
    mock_requests.post.assert_called_once_with(url, data=payload, headers=headers)


@pytest.mark.integration
@patch("apps.CertsGen.requests")
def test_register_recipient(mock_requests):
    token = "wkrmspr131refal2345"
    owner = "0x8C7a749EDf3C441d91c18b118f7768f4022759d9"
    first_name = "Miguel"
    last_name = "Mendez"
    id_number = 5678
    id = "V-23555449"
    email = "immendez196@gmail.com"
    register_recipient(token, owner, first_name, last_name, id, id_number, email)
    headers = { "Authorization": "Token {}".format(token)}
    payload = {
        	'owner': owner,
        	'name': '%s' %first_name+' '+last_name,
            'id_number': 1000+id_number,
        	'id': id,
        	'email': email,
    }
    url = f"{settings.CERTSGEN_URL}/api/register/recipient/"
    mock_requests.post.assert_called_once_with(url, json=payload, headers=headers)


@pytest.mark.integration
@patch("apps.CertsGen.requests")
def test_register_certificate(mock_requests):
    token = "wkrmspr131refal2345"
    recipient_address = "0x8C7a749EDf3C441d91c18b118f7768f4022759d9"
    titulo = "Notas Certificadas"
    descripcion = "Notas Certificadas de Ing. de Sistemas"
    register_certificate(token, recipient_address, titulo, descripcion)
    headers = { "Authorization": "Token {}".format(token)}
    payload = {
        'recipient_address': recipient_address,
        'title': titulo,
        'description': descripcion
    }
    url = f"{settings.CERTSGEN_URL}/api/register/certificate/"
    mock_requests.post.assert_called_once_with(url, json=payload, headers=headers)


@pytest.mark.integration
@patch("apps.CertsGen.requests")
def test_add_signature(mock_requests):
    token = "wkrmspr131refal2345"
    certificate_address = "0x9E25bC7236df52E78fB47c03e8e785cAE9f3A2d0"
    first_name = "Miguel"
    last_name = "Mendez"
    add_signature(token, certificate_address, first_name, last_name)
    headers = { "Authorization": "Token {}".format(token)}
    payload = {
        'certificate_address': certificate_address,
        'params': f'P.A. {first_name} {last_name}'
    }
    url = f"{settings.CERTSGEN_URL}/api/add/signature/"
    mock_requests.post.assert_called_once_with(url, json=payload, headers=headers)


@pytest.mark.integration
@patch("apps.CertsGen.requests")
def test_add_denpendency(mock_requests):
    token = "wkrmspr131refal2345"
    certificate_address = "0x9E25bC7236df52E78fB47c03e8e785cAE9f3A2d0"
    from_owner = "0x7BaA7C3294EDF61b054e47cfA96e8a5dF4144b73"
    to_owner = "0x9303B427bC0f137605724dBeAf099908bD6B8f1d"
    add_denpendency(token, certificate_address, from_owner, to_owner)
    headers = { "Authorization": "Token {}".format(token)}
    payload = {
                'certificate_address': certificate_address,
                'from_owner': from_owner,
                'to_owner': to_owner
    }
    url = f"{settings.CERTSGEN_URL}/api/add/certifier-dependency/"
    mock_requests.post.assert_called_once_with(url, json=payload, headers=headers)


@pytest.mark.integration
@patch("apps.CertsGen.requests")
def test_get_certificates(mock_requests):
    token = "wkrmspr131refal2345"
    get_certificates(token)
    headers = { "Authorization": "Token {}".format(token)}
    url = f"{settings.CERTSGEN_URL}/api/get/certificates/"
    mock_requests.get.assert_called_once_with(url, headers=headers)