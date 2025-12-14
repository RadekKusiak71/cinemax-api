import pytest
from django.core.exceptions import ValidationError

from core.factories import LanguageFactory
from core.models import Language

pytestmark = pytest.mark.django_db


def test_language_str_repr(language: Language):
    assert str(language) == f'{language.name} ({language.code})'

def test_language_code_uniqueness(language: Language, language_factory: LanguageFactory):
    with pytest.raises(ValidationError) as exc_info:
        new_language: Language = language_factory.build(code=language.code)
        new_language.full_clean()
    
    assert 'code' in exc_info.value.message_dict
    assert exc_info.value.message_dict['code'] == ['Language with this Code already exists.']

def test_language_name_uniqueness(language: Language, language_factory: LanguageFactory):
    with pytest.raises(ValidationError) as exc_info:
        new_language: Language = language_factory.build(name=language.name)
        new_language.full_clean()
    
    assert 'name' in exc_info.value.message_dict
    assert exc_info.value.message_dict['name'] == ['Language with this Name already exists.']