import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#Enable or disable request and response logging
ENABLE_REQUEST_LOGGING = True
ENABLE_RESPONSE_LOGGING = True
# Log only specific API paths (prefixes)
LOG_SPECIFIC_PATHS = [
    '/api/users/',
    '/api/orders/',
]

# Log only responses with these status codes
LOG_STATUS_CODES = [400, 404, 500]

# Enable SQL query logging for slow queries
LOG_SQL_QUERIES = True
SLOW_QUERY_THRESHOLD = 0.5  # Log queries that take longer than 0.5 seconds

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'info_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/info.log'),
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            # 'class': 'logging.FileHandler',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/error.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,  # Keep up to 5 backup files
            'formatter': 'verbose',
        },
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'info_file','error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'evchargingapi': {
            'handlers': ['debug_file', 'error_file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        # 'django': {
        #     'handlers': ['console', 'info_file', 'error_file', 'debug_file'],
        #     'level': 'DEBUG',
        #     'propagate': False,
        # },
    },
}
