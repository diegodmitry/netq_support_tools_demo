class IntegrationClientError(Exception):
    pass


class IntegrationTimeoutError(IntegrationClientError):
    pass


class IntegrationTransportError(IntegrationClientError):
    pass


class IntegrationHTTPStatusError(IntegrationClientError):
    def __init__(self, status_code: int, body: str) -> None:
        self.status_code = status_code
        self.body = body
        super().__init__(f"Integration request failed with status {status_code}")
