import json
import logging
import time
from django.conf import settings
from django.db import connection
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('django')

class AdvancedLoggingMiddleware(MiddlewareMixin):
    SENSITIVE_FIELDS = {'password', 'token', 'api_key'}
    MAX_RESPONSE_BODY_SIZE = 1024  # Max response size for logging (in bytes)

    def __init__(self, get_response):
        self.get_response = get_response
        self.enable_request_logging = getattr(settings, 'ENABLE_REQUEST_LOGGING', False)
        self.enable_response_logging = getattr(settings, 'ENABLE_RESPONSE_LOGGING', False)
        self.log_specific_paths = getattr(settings, 'LOG_SPECIFIC_PATHS', [])
        self.log_sql_queries = getattr(settings, 'LOG_SQL_QUERIES', False)
        self.slow_query_threshold = getattr(settings, 'SLOW_QUERY_THRESHOLD', 0.5)  # Threshold in seconds
        self.log_status_codes = getattr(settings, 'LOG_STATUS_CODES', [500])  # Only log responses with these status codes


    def __call__(self, request):
        start_time = time.time()

        if self.should_log_request(request):
            self.log_request(request)

        try:
            response = self.get_response(request)
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Exception occurred: {str(e)} | Duration: {duration:.2f}s", exc_info=True)
            raise

        duration = time.time() - start_time

        if self.should_log_response(response):
            self.log_response(response, duration)

        if self.log_sql_queries and duration > self.slow_query_threshold:
            self.log_slow_queries(duration)

        return response

    def should_log_request(self, request):
        """Check if the request path matches the specific paths to log, or log all if the list is empty."""
        if not self.log_specific_paths:
            return True
        return any(request.path.startswith(path) for path in self.log_specific_paths)

    def should_log_response(self, response):
        """Check if the response status code is in the list of status codes to log."""
        return response.status_code in self.log_status_codes or (self.enable_response_logging and response.status_code < 500)

    def log_request(self, request):
        """Log request details, masking sensitive fields."""
        request_details = {
            'method': request.method,
            'path': request.path,
            'ip': self.get_client_ip(request),
            'headers': self.get_headers(request),
        }

        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                body = json.loads(request.body.decode('utf-8'))
                request_details['body'] = self.mask_sensitive_data(body)
            except Exception:
                request_details['body'] = 'Unable to parse body'

        logger.info(f"Request: {json.dumps(request_details)}")

    def log_response(self, response, duration):
        """Log response details, including duration and body if it is within the size limit."""
        response_details = {
            'status_code': response.status_code,
            'duration': f"{duration:.2f}s",
        }

        if response.get('content-type') == 'application/json':
            body_size = len(response.content)
            if body_size <= self.MAX_RESPONSE_BODY_SIZE:
                try:
                    response_details['body'] = json.loads(response.content.decode('utf-8'))
                except Exception:
                    response_details['body'] = 'Unable to parse response body'
            else:
                response_details['body'] = f'Response body too large to log ({body_size} bytes)'

        logger.info(f"Response: {json.dumps(response_details)}")

    def log_slow_queries(self, duration):
        """Log SQL queries if the request took longer than the slow query threshold."""
        queries = connection.queries
        slow_queries = [q for q in queries if float(q['time']) > self.slow_query_threshold]
        for query in slow_queries:
            logger.warning(f"Slow Query ({query['time']}s): {query['sql']}")

    def get_client_ip(self, request):
        """Get the client's IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_headers(self, request):
        """Get headers from the request, excluding sensitive ones."""
        excluded_headers = {'Authorization', 'Cookie'}
        headers = {k: v for k, v in request.META.items() if k.startswith('HTTP_') and k[5:] not in excluded_headers}
        return {k[5:].replace('_', '-').title(): v for k, v in headers.items()}

    def mask_sensitive_data(self, data):
        """Mask sensitive fields in the request body."""
        if isinstance(data, dict):
            return {
                key: ('*****' if key.lower() in self.SENSITIVE_FIELDS else self.mask_sensitive_data(value))
                for key, value in data.items()
            }
        elif isinstance(data, list):
            return [self.mask_sensitive_data(item) for item in data]
        return data
