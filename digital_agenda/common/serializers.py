from rest_framework import serializers


class CodeRelatedField(serializers.SlugRelatedField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("slug_field", "code")
        kwargs.setdefault("read_only", True)

        super().__init__(*args, **kwargs)
