from rest_framework import serializers


class RequestUserMixin(object):
    def get_current_user(self):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return request.user
        return None


class BaseModelSerializer(serializers.ModelSerializer, RequestUserMixin):
    pass


class BaseSerializer(serializers.Serializer, RequestUserMixin):
    pass
