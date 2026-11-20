from urllib.parse import urlparse

from django.core.exceptions import ValidationError


def validate_github_url(value):
    """Accept only HTTP(S) links hosted on GitHub's main domain."""
    parsed_url = urlparse(value)
    if (
        parsed_url.scheme not in ("http", "https")
        or parsed_url.hostname not in ("github.com", "www.github.com")
        or parsed_url.username
        or parsed_url.password
    ):
        raise ValidationError("Ссылка должна вести на github.com")
