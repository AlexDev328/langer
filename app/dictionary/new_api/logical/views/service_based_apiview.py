from rest_framework.generics import GenericAPIView

from dictionary.new_api.logical.views import mixins


class ServiceBasedAPIView(GenericAPIView):
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


class ServiceCreateAPIView(mixins.CreateModelMixin,
                           ServiceBasedAPIView):
    """
    Concrete view for creating a model instance.
    """

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ServiceListAPIView(mixins.ListModelMixin,
                         ServiceBasedAPIView):
    """
    Concrete view for listing a queryset.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ServiceRetrieveAPIView(mixins.RetrieveModelMixin,
                             ServiceBasedAPIView):
    """
    Concrete view for retrieving a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class ServiceDestroyAPIView(mixins.DestroyModelMixin,
                            ServiceBasedAPIView):
    """
    Concrete view for deleting a model instance.
    """

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ServiceUpdateAPIView(mixins.UpdateModelMixin,
                           ServiceBasedAPIView):
    """
    Concrete view for updating a model instance.
    """

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ServiceListCreateAPIView(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               ServiceBasedAPIView):
    """
    Concrete view for listing a queryset or creating a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ServiceRetrieveUpdateAPIView(mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   ServiceBasedAPIView):
    """
    Concrete view for retrieving, updating a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ServiceRetrieveDestroyAPIView(mixins.RetrieveModelMixin,
                                    mixins.DestroyModelMixin,
                                    ServiceBasedAPIView):
    """
    Concrete view for retrieving or deleting a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ServiceRetrieveUpdateDestroyAPIView(mixins.RetrieveModelMixin,
                                          mixins.UpdateModelMixin,
                                          mixins.DestroyModelMixin,
                                          ServiceBasedAPIView):
    """
    Concrete view for retrieving, updating or deleting a model instance.
    """

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
