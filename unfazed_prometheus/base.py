import os

from starlette.types import Scope
from unfazed.conf import settings

from .decorators import Decorator, meta_monitor
from .metrics import (
    ApiCallCounter,
    ApiCallDurationHistogram,
    CacheCounter,
    CacheDurationHistogram,
    DatabaseCounter,
    DatabaseDurationHistogram,
    ExceptionCounter,
    FunctionCounter,
    FunctionDurationHistogram,
    RequestCounter,
    RequestDurationHistogram,
)
from .settings import PrometheusSettings
from .utils import get_first_arg_first_letter, get_first_arg_name, get_function_name


class Agent:
    def __init__(self) -> None:
        self._ready = False

    @property
    def settings(self) -> PrometheusSettings:
        return settings["UNFAZED_PROMETHEUS_SETTINGS"]

    def setup(self) -> None:
        # check prometheus multiproc dir settings
        if self.settings.prometheus_multiproc_dir:
            if (
                "PROMETHEUS_MULTIPROC_DIR" not in os.environ
                or "prometheus_multiproc_dir" not in os.environ
            ):
                os.environ["PROMETHEUS_MULTIPROC_DIR"] = (
                    self.settings.prometheus_multiproc_dir
                )

        self._ready = True

    def check_ready(self) -> None:
        if not self._ready:
            self.setup()

    @property
    def monitor_function(self) -> Decorator:
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

    def monitor_api(self, endpoint: str, category: str = "api") -> Decorator:
        self.check_ready()

        return meta_monitor(
            counter_handler=ApiCallCounter,
            hist_handler=ApiCallDurationHistogram,
            exc_handler=ExceptionCounter,
            counter_labels=[self.settings.project, self.settings.hostname, endpoint],
            hist_labels=[self.settings.project, self.settings.hostname, endpoint],
            exc_labels=[self.settings.project, self.settings.hostname, category],
        )

    def monitor_request(self, scope: Scope) -> Decorator:
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

    @property
    def monitor_database(self) -> Decorator:
        self.check_ready()

        return meta_monitor(
            counter_handler=DatabaseCounter,
            hist_handler=DatabaseDurationHistogram,
            exc_handler=ExceptionCounter,
            counter_labels=[
                self.settings.project,
                self.settings.hostname,
                get_first_arg_first_letter,
            ],
            hist_labels=[
                self.settings.project,
                self.settings.hostname,
                get_first_arg_first_letter,
            ],
            exc_labels=[self.settings.project, self.settings.hostname, "database"],
        )

    @property
    def monitor_cache(self) -> Decorator:
        self.check_ready()

        return meta_monitor(
            counter_handler=CacheCounter,
            hist_handler=CacheDurationHistogram,
            exc_handler=ExceptionCounter,
            counter_labels=[
                self.settings.project,
                self.settings.hostname,
                get_first_arg_name,
            ],
            hist_labels=[
                self.settings.project,
                self.settings.hostname,
                get_first_arg_name,
            ],
            exc_labels=[self.settings.project, self.settings.hostname, "cache"],
        )


agent: Agent = Agent()
