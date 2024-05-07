from flask import request

def is_active(endpoint):
    if request.endpoint == endpoint:
        return 'active'
    return ''