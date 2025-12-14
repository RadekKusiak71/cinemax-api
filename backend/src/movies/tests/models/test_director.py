import pytest
from movies.models import Director

pytestmark = pytest.mark.django_db

def test_director_str_repr(director: Director) -> None:
    assert str(director) == f"{director.first_name} {director.last_name}"
