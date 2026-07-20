from backend.libs.settings.core import CoreSettings


class ServiceSettings(CoreSettings):
    """
    Service/runtime settings for HTTP-facing applications.
    Defines application identity and networking configuration.
    """

    # Application identity
    app_name: str
    app_version: str = "0.1.0"

    # Networking
    app_host: str = "0.0.0.0"
    app_port: int = 8000
