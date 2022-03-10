from test.models import Blog
from .serializers import BlogSerializer

# Import your package here.

from drf_localize.commons.helpers.views import (
    BasicModelViewSet
)


# Create your views here.

class BlogViewSet(BasicModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
