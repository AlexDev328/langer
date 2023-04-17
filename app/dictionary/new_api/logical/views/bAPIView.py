from rest_framework.generics import GenericAPIView


class BApiView(GenericAPIView):
    # You'll need to either set service_class attribute,
    # or override `get_service_class()`.
    service_class = None

    def get_service(self, *args, **kwargs):
        service_class = self.get_service_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return service_class(*args, **kwargs)

    def get_service_class(self):
        assert self.service_class is not None, (
                "'%s' should either include a `service_class` attribute, "
                "or override the `get_service_class()` method."
                % self.__class__.__name__
        )

        return self.service_class

    def get_service_context(self):
        """
        Extra context provided to the service class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }
