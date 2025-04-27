from pydantic import BaseModel, Field
from unfazed.conf import register_settings


@register_settings("UNFAZED_PROMETHEUS_SETTINGS")
class PrometheusSettings(BaseModel):
    """
    settings key: UNFAZED_PROMETHEUS_SETTINGS

    """

    project: str = Field(alias="PROJECT")
    hostname: str = Field(alias="HOSTNAME")
    prometheus_multiproc_dir: str | None = Field(
        default=None, alias="PROMETHEUS_MULTIPROC_DIR"
    )
