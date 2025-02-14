from pydantic import BaseModel, Field


class PrometheusSettings(BaseModel):
    project: str = Field(alias="PROJECT")
    hostname: str = Field(alias="HOSTNAME")
    prometheus_multiproc_dir: str = Field(
        default=None, alias="PROMETHEUS_MULTIPROC_DIR"
    )
