from typing import Type


class BaseValidation:
    """
    A base class from which all permission classes should inherit.
    """

    def is_valid(self, data, *args, **kwargs):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True


class TestValidation(BaseValidation):

    def is_valid(self, data, *args, **kwargs):
        return True


class BaseService:
    validation_classes = []
    model = None

    def __init__(self, data, instance=None, *args, **kwargs):
        self.data = data
        self.instance = instance
        self.valid = None
        self.context = kwargs.get('context', {})

    def is_valid(self, raise_exception=False):
        for v in self.validation_classes:
            if not v().is_valid(self.data):
                if raise_exception:
                    raise Exception()
                self.valid = False
                return False
        self.valid = True
        return True

    def save(self, **kwargs):
        if self.instance:
            return self.update(**kwargs)
        else:
            return self.create(**kwargs)

    def create(self, **kwargs):
        return self.model.objects.create(**self.data.update(kwargs))

    def update(self, **kwargs):
        for attr, value in self.data.items():
            setattr(self.instance, attr, value)
        for attr, value in kwargs.items():
            setattr(self.instance, attr, value)
        self.instance.save()
        return self.instance

    def destroy(self, **kwargs):
        self.instance.delete()
