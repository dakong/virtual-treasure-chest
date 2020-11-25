# Implemented according to the [JSend specfication](https://github.com/omniti-labs/jsend)

def generateSuccessResponse(data):
    return {
        'status': 'success',
        'data': data
    }


def generateErrorResponse(message, code=None, data=None):
    response = {
        'status': 'error',
        'message': message
    }
    if code != None:
        response['code'] = code
    if data != None:
        response['data'] = data

    return response


def generateFailResponse(data):
    return {
        'status': 'fail',
        'data': data
    }
