from test.models import Blog

# Import your package here.

from drf_localize.commons.serializers import (
    I18NModelSerializer
)


# Create your serializers here.


class BlogSerializer(I18NModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
