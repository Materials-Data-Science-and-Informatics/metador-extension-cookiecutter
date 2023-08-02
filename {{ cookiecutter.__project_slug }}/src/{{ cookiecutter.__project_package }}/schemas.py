"""Metador schema plugins provided by this package."""
from metador_core.schema import MetadataSchema
from metador_core.schema.types import Int, Str


class MyCustomSchema(MetadataSchema):
    """This is a simple example Metador schema plugin."""

    class Plugin:
        name = "acme.custom-schema"
        version = (0, 1, 0)

    magic_number: Int
    some_text: Str = "(no text)"
