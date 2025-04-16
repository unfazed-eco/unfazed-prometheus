Unfazed Prometheus
====


## Installation

```bash

pip install unfazed-prometheus


```


## Quick Start


### Add Settings


```python

# settings.py
import socket

UNFAZED_PROMETHEUS_SETTINGS = {
    "HOSTNAME": socket.gethostname(),
    "PROJECT": "{{ project_name }}",
    "PROMETHEUS_MULTIPROC_DIR": "/prometheus",
}


# add lifespan

UNFAZED_SETTINGS = {
    # ... other settings
    "LIFESPAN": ["unfazed_prometheus.lifespan.PrometheusLifespan"],
}

```


### Monitor Request

all you need to do is add the middleware to the middleware list.

```python


UNFAZED_SETTINGS = {
    # ... other settings
    "MIDDLEWARE": [
        "unfazed_prometheus.middleware.common.PrometheusHttpRequestMiddleware",
    ],
}

```


### Monitor Database using Tortoise ORM

all you need to do is to use the `unfazed_prometheus.database.tortoise.mysql` database engine.

```python

UNFAZED_SETTINGS = {
    "DATABASE": {
        "CONNECTIONS": {
            "default": {
                "ENGINE": "unfazed_prometheus.database.tortoise.mysql",
                "CREDENTIALS": {
                    "HOST": "mysql",
                    "PORT": 3306,
                    "USER": "app",
                    "PASSWORD": "app",
                    "DATABASE": "app",
                },
            }
        },
    },


}

```


### Monitor Cache 


all you need to do is to use the `unfazed_prometheus.cache.backends.default.PrometheusDefaultBackend` cache backend.


```python

UNFAZED_SETTINGS = {
    "CACHE": {
        "default": {
            "BACKEND": "unfazed_prometheus.cache.backends.default.PrometheusDefaultBackend",
            "LOCATION": "redis://redis:6379",
            "OPTIONS": {
                "decode_responses": True,
                "max_connections": 1000,
            },
        }
    },
}

```


### Monitor Function


use prometheus agent.monitor_function decorator.


```python


from unfazed_prometheus import agent


@agent.monitor_function
def my_function(a: int, b: int) -> int:
    return a + b

```


### Monitor API


use prometheus agent.monitor_api decorator.


```python


from unfazed_prometheus import agent


@agent.monitor_api("/api/v1/users")
async def get_users():
    resp = await asyncrequests.get("https://api.github.com/users")
    return resp.json()


```


### Monitor Exception

unfazed_prometheus will monitor exceptions through other monitor decorators. all you need to do is to let the exception be raised or raise it yourself.


```python

from module import CustomException

@agent.monitor_function
def devide(a: int, b: int) -> float:
    if b == 0:
        raise CustomException("b is 0")

    return a / b


```

or just let the exception be raised.


```python

@agent.monitor_function
def devide(a: int, b: int) -> float:
    return a / b

```

unfazed_prometheus will automatically collect the exception and count the total number of exceptions.

## connect to prometheus server


in the live env, it's better to connect to prometheus server use another service other than the unfazed server.


example code see [scripts/prometheus_client.py](scripts/prometheus_client.py)


## Advanced


if the default metrics and decorators cannot meet your needs, `meta_monitor` may help.


```python

from prometheus_client import Counter, Histogram
from unfazed_prometheus import meta_monitor


counter = Counter(
    "my_counter",
    "my_counter_description",
    ["label1", "label2"],
)


my_monitor = meta_monitor(
    counter_handler=counter,
    counter_labels=["foo", "bar"],
)


@my_monitor
def my_function(a: int, b: int) -> int:
    return a + b


```

meta_monitor signature:

```python

def meta_monitor(
    counter_handler: t.Optional[Counter] = None,
    hist_handler: t.Optional[Histogram] = None,
    exc_handler: t.Optional[Counter] = None,
    counter_labels: t.Optional[Labels] = None,
    hist_labels: t.Optional[Labels] = None,
    exc_labels: t.Optional[Labels] = None,
) -> Decorator:

    ...

```




