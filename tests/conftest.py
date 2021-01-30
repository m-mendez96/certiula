import django
import pytest

django.setup()
pytestmark = pytest.mark.django_db