"""Tools for integrating with RATOC and ROHM J11 B-route adapters."""

from .codec import ChecksumError, FrameFormatError, ProtocolError
from .commands import CommandFailedError, CredentialFormatError
from .echonet import EchonetFrameError, MeterProfile
from .session import (
    AuthenticationError,
    BackoffPolicy,
    CachedNetwork,
    J11Session,
    MeterLink,
    MeterNotFoundError,
    MeterReading,
    NetworkCache,
    SessionClosedError,
    SessionConfig,
    SessionError,
    SessionStats,
    SessionTimeoutError,
    TransmissionError,
)
from .transport import ByteTransport, SerialTransport, TransportError

__version__ = "0.1.0"

__all__ = [
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
]
