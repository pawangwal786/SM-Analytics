import logging

from backend.libs.observability.context.vars import get_correlation_id, get_request_id


class ContextInjectionFilter(logging.Filter):
    """
    Injects request_id, correlation_id, service name, and environment
    into every log record automatically.
    """

    def __init__(self, service: str, environment: str):
        super().__init__()
        self.service = service
        self.environment = environment

    def filter(self, record: logging.LogRecord) -> bool:
        record.service = self.service
        record.environment = self.environment

        req_id = get_request_id()
        if req_id:
            record.request_id = req_id

        corr_id = get_correlation_id()
        if corr_id:
            record.correlation_id = corr_id

        return True
