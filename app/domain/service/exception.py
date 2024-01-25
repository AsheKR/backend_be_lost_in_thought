class ServiceException(Exception):
    pass


class DoesNotExist(ServiceException):
    pass
