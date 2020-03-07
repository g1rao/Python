import threading
import logging
from django.utils.deprecation import MiddlewareMixin

local = threading.local()

class CustomLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        remote_addr = request.META['REMOTE_ADDR']
        setattr(local, 'remote_addr', remote_addr)

class CustomLoggingFilter(logging.Filter):
    def filter(self, record):        
        record.remote_addr = getattr(local, 'remote_addr', 'no host')
        return True

# Configure filters 
LOCAL_SETTINGS = ""
