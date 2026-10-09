import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


NSFW_SERVICE_URL = "http://localhost:6086/api"


# One Session per Python process.
# Celery worker processes will each have their own Session.
session = requests.Session()


retry = Retry(
    total=3,
    connect=3,
    read=3,
    status=3,
    backoff_factor=1,

    # Retry when the NSFW service is temporarily unavailable.
    status_forcelist=(502, 503, 504),

    # Don't retry every HTTP method.
    allowed_methods=("POST",),
)


adapter = HTTPAdapter(
    max_retries=retry,
    pool_connections=20,
    pool_maxsize=20,
)


session.mount("http://", adapter)
session.mount("https://", adapter)
session.headers.update({
    'Authorization':'Bearer your_token_here'
})


def check_nsfw(file):
    response = session.post(
        f"{NSFW_SERVICE_URL}/upload_check",
        files={
            "file": file,
        },
        timeout=30,
    )

    response.raise_for_status()

    return response.json()