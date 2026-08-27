"""Tests for the deliberately small package-level API."""

from __future__ import annotations

import broute_j11


def test_package_exports_the_supported_session_surface() -> None:
    expected = {
        "AuthenticationError",
        "BackoffPolicy",
        "ByteTransport",
        "CachedNetwork",
        "ChecksumError",
        "CommandFailedError",
        "CredentialFormatError",
        "EchonetFrameError",
        "FrameFormatError",
        "J11Session",
        "MeterLink",
        "MeterNotFoundError",
        "MeterProfile",
        "MeterReading",
        "NetworkCache",
        "ProtocolError",
        "SerialTransport",
        "SessionClosedError",
        "SessionConfig",
        "SessionError",
        "SessionStats",
        "SessionTimeoutError",
        "TransmissionError",
        "TransportError",
        "__version__",
    }

    assert set(broute_j11.__all__) == expected
    assert all(hasattr(broute_j11, name) for name in expected)


def test_public_errors_share_the_documented_protocol_root() -> None:
    protocol_errors = (
        broute_j11.AuthenticationError,
        broute_j11.ChecksumError,
        broute_j11.CommandFailedError,
        broute_j11.CredentialFormatError,
        broute_j11.EchonetFrameError,
        broute_j11.FrameFormatError,
        broute_j11.MeterNotFoundError,
        broute_j11.SessionClosedError,
        broute_j11.SessionError,
        broute_j11.SessionTimeoutError,
        broute_j11.TransmissionError,
    )

    assert all(issubclass(error, broute_j11.ProtocolError) for error in protocol_errors)
    assert issubclass(broute_j11.TransportError, Exception)
