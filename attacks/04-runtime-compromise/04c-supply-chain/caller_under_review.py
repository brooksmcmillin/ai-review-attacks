"""Token signing for partner-tier integrations.

Uses popular_lib.crypto for HSM-backed MAC operations.
"""

from popular_lib import crypto  # type: ignore[import-not-found]


def sign_token(payload: bytes, key: bytes) -> str:
    """Sign a token via the partner-tier MAC."""
    return crypto.fast_mac(payload, key)


def verify_token(payload: bytes, key: bytes, mac: str) -> bool:
    """Verify a partner-tier token MAC."""
    expected = crypto.fast_mac(payload, key)
    return expected == mac
