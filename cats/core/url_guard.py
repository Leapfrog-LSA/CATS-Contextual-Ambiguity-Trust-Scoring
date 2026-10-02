"""Refuse fetches that would reach non-public addresses (threat model T9).

``score_feed``, the MCP tool ``score_source`` and the RSS collector fetch URLs
supplied by a caller — through the MCP server, by an LLM that prompt injection
can steer. Without a check, such a URL can point at loopback, a private
network or a cloud metadata endpoint (``169.254.169.254``).

:func:`check_url` resolves the host and refuses the URL unless **every**
address it resolves to is globally routable. Callers re-check each redirect
hop, so a public URL cannot bounce to an internal one.

Residual risk: the address is resolved here and again by the HTTP client, so a
DNS-rebinding host that answers differently between the two lookups is not
stopped. Closing that gap needs connection-level IP pinning.

Standard library only, so the collector keeps running with a minimal install.
"""

import ipaddress
import socket
from typing import List
from urllib.parse import urlsplit

_ALLOWED_SCHEMES = frozenset({"http", "https"})


class UnsafeURLError(ValueError):
    """The URL's scheme is not http(s), or its host resolves to a non-public address."""


def _resolve_host(host: str) -> List[str]:
    """All addresses ``host`` resolves to (module-level so tests can replace it)."""
    infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    return sorted({str(info[4][0]) for info in infos})


def _is_public(address: str) -> bool:
    ip = ipaddress.ip_address(address.split("%", 1)[0])  # drop an IPv6 zone id
    if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped is not None:
        ip = ip.ipv4_mapped
    return ip.is_global and not ip.is_multicast


def check_url(url: str, *, allow_private: bool = False) -> None:
    """Raise :class:`UnsafeURLError` unless ``url`` is http(s) on a public host.

    ``allow_private=True`` keeps the scheme check but skips the address check,
    for a caller that deliberately scores feeds on its own network.

    A host that does not resolve is let through: the fetch then fails as an
    ordinary unreachable host, which is the error the caller should see.
    """
    parts = urlsplit(url)
    if parts.scheme.lower() not in _ALLOWED_SCHEMES:
        raise UnsafeURLError(f"refused {url!r}: only http and https URLs can be fetched")
    host = parts.hostname
    if not host:
        raise UnsafeURLError(f"refused {url!r}: no host")
    if allow_private:
        return
    try:
        addresses = _resolve_host(host)
    except (socket.gaierror, UnicodeError):
        return
    blocked = [a for a in addresses if not _is_public(a)]
    if blocked:
        raise UnsafeURLError(f"refused {url!r}: {host} resolves to a non-public address ({', '.join(blocked)})")
