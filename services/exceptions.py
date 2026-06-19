class BusinessError(Exception):
    """Base class for all business/validation errors in the service layer."""
    pass

class ValidationError(BusinessError):
    """Raised when form validations or business rules fail."""
    def __init__(self, message, context_id=None):
        super().__init__(message)
        self.context_id = context_id

class ResourceNotFoundError(BusinessError):
    """Raised when a requested resource (e.g. Patient, Group) is not found."""
    pass
