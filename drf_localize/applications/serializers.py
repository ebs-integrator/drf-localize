from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    PrimaryKeyRelatedField
)

# Import your package here.

from drf_localize.models import (
    LocalizeApplication,
)
from drf_localize.models import (
    LocalizeLanguage,
)


# Create your serializers here.


class LocalizeApplicationSerializer(ModelSerializer):
    class Meta:
        model = LocalizeApplication
        fields = [
            'id',
            'hash',
            'title',
            'description'
        ]


class LocalizeApplicationLanguageSerializer(Serializer):
    languages_id = PrimaryKeyRelatedField(
        queryset=LocalizeLanguage.objects.filter(),
        required=True,
        many=True,
    )

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
