from laptimer.models import ApiResult

# API helper functions

def check_if_found(calling_object, calling_method, name):
    '''
    Checks to ensure that an object with specified name doesn't already exist
    in the database. If the calling Django object does exists, method returns
    a failed ApiResult with error message, otherwise returns True.
    '''
    if calling_object.objects.filter(name=name).exists():
        error = '%s already exists' % calling_object.__name__ # TODO: i18n
        return ApiResult(calling_method, ok=False, data=error)
    return True

def check_if_not_found(calling_object, calling_method, name):
    '''
    Checks to ensure that an object with specified name already exists in the
    database. If the calling Django object does not exist, method returns a
    failed ApiResult with error message, otherwise returns True.
    '''
    if not calling_object.objects.filter(name=name).exists():
        error = '%s not found' % calling_object.__name__ # TODO: i18n
        return ApiResult(calling_method, ok=False, data=error)
    return True
