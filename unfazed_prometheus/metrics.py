from prometheus_client import Counter, Histogram

# http request
RequestCounter = Counter(
    "request_total",
    "Total number of requests",
    labelnames=["project", "hostname", "method", "path"],
)


RequestDurationHistogram = Histogram(
    "request_duration_seconds",
    "Duration of requests",
    labelnames=["project", "hostname", "method", "path"],
)


# exception
ExceptionCounter = Counter(
    "exception_total",
    "Total number of exceptions",
    labelnames=["project", "hostname", "category"],
)


# database
DatabaseCounter = Counter(
    "database_request_total",
    "Total number of database operations",
    labelnames=["project", "hostname", "category"],
)


DatabaseDurationHistogram = Histogram(
    "database_duration_seconds",
    "Duration of database operations",
    labelnames=["project", "hostname", "category"],
)

DatabaseConnectionCounter = Counter(
    "database_connection_total",
    "Total number of database connections",
    labelnames=["project", "hostname", "category"],
)


# cache
CacheCounter = Counter(
    "cache_request_total",
    "Total number of cache operations",
    labelnames=["project", "hostname", "category"],
)

CacheDurationHistogram = Histogram(
    "cache_duration_seconds",
    "Duration of cache operations",
    labelnames=["project", "hostname", "category"],
)

CacheConnectionCounter = Counter(
    "cache_connection_total",
    "Total number of cache connections",
    labelnames=["project", "hostname", "category"],
)


# Function
FunctionCounter = Counter(
    "function_total",
    "Total number of function calls",
    labelnames=["project", "hostname", "function_name"],
)

FunctionDurationHistogram = Histogram(
    "function_duration_seconds",
    "Duration of function calls",
    labelnames=["project", "hostname", "function_name"],
)


# api call
ApiCallCounter = Counter(
    "api_call_total",
    "Total number of api calls",
    labelnames=["project", "hostname", "endpoint"],
)

ApiCallDurationHistogram = Histogram(
    "api_call_duration_seconds",
    "Duration of api calls",
    labelnames=["project", "hostname", "endpoint"],
)
