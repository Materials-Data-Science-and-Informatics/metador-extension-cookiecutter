import pytest
from metador_core.plugins import schemas
from pydantic import ValidationError


def test_custom_schema():
    MySchema = schemas["acme.custom-schema"]

    with pytest.raises(ValidationError):
        MySchema()  # missing magic_number field

    # valid instance is as expected
    expected = dict(magic_number=1, some_text="hello")
    assert MySchema(magic_number=1, some_text="hello").dict() == expected
