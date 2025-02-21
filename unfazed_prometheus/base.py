import os

from starlette.types import Scope
from unfazed.conf import settings

from .decorators import meta_monitor
from .metrics import (
    ApiCallCounter,
    ApiCallDurationHistogram,
    ExceptionCounter,
    FunctionCounter,
    FunctionDurationHistogram,
    RequestCounter,
    RequestDurationHistogram,
)
from .settings import PrometheusSettings
from .utils import get_function_name


class Agent:
    def __init__(self):
        self.settings: PrometheusSettings = settings["UNFAZED_PROMETHEUS_SETTINGS"]
        self._ready = False

    def setup(self):
        # check prometheus path settings
        if self.settings.prometheus_path:
            path = self.settings.prometheus_path

        else:
            path = os.getenv("prometheus_multiproc_dir") or os.getenv(
                "PROMETHEUS_MULTIPROC_DIR"
            )

        if not path:
            raise ValueError("prometheus_multiproc_dir is not set")

        if not os.path.exists(path):
            raise FileNotFoundError(f"Prometheus metrics file not found at {path}")

        os.environ["PROMETHEUS_MULTIPROC_DIR"] = path

        self._ready = True

    def check_ready(self):
        if not self._ready:
            raise RuntimeError(
                "Unfazed Prometheus is not ready, set `unfazed_prometheus.lifespan.PrometheusLifespan` in your lifespan settings."
            )

    @property
    def monitor_function(self):
        self.check_ready()
        return meta_monitor(
            counter_handler=FunctionCounter,
            hist_handler=FunctionDurationHistogram,
            exc_handler=ExceptionCounter,
            counter_labels=[
                self.settings.project,
                self.settings.hostname,
                get_function_name,
            ],
            hist_labels=[
                self.settings.project,
                self.settings.hostname,
                get_function_name,
            ],
            exc_labels=[self.settings.project, self.settings.hostname, "function"],
        )

    def monitor_api(self, endpoint: str, category: str = "api"):
        self.check_ready()
        return meta_monitor(
            counter_handler=ApiCallCounter,
            hist_handler=ApiCallDurationHistogram,
            exc_handler=ExceptionCounter,
            counter_labels=[self.settings.project, self.settings.hostname, endpoint],
            hist_labels=[self.settings.project, self.settings.hostname, endpoint],
            exc_labels=[self.settings.project, self.settings.hostname, category],
        )

    def monitor_request(self, scope: Scope):
        self.check_ready()
        return meta_monitor(
            counter_handler=RequestCounter,
            hist_handler=RequestDurationHistogram,
            counter_labels=[
                self.settings.project,
                self.settings.hostname,
                scope["method"],
                scope["path"],
            ],
            hist_labels=[
                self.settings.project,
                self.settings.hostname,
                scope["method"],
                scope["path"],
            ],
        )


agent = Agent()
