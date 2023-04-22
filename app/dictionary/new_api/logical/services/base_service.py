class BaseValidation:
    """
    A base class from which all permission classes should inherit.
    """

    def is_valid(self, data, *args, **kwargs):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True


class BaseValidation:

    def is_valid(self, data, *args, **kwargs):
        return True


class BaseService:
    validation_classes = []
    model = None

    def __init__(self, data, *args, **kwargs):
        self.data = data
        self.valid = None

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
        pass
