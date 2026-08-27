# broute-j11

`broute-j11` is an MIT-licensed Python library for communicating with Japanese
B-route smart electricity meters through binary-UART J11 adapters. It is
intended to provide reusable framing, command, ECHONET Lite, serial transport,
and asynchronous session layers without depending on Home Assistant.

> [!IMPORTANT]
> Version 0.1.0 establishes the package and release infrastructure. The public
> protocol API is not included yet. Do not install this release expecting
> hardware communication.

## Supported hardware

Initial protocol support is deliberately scoped to:

- RATOC Systems RS-WSUHA-J11;
- ROHM BP35C2-J11-T01; and
- other BP35C0-J11-based adapters after their USB and UART behavior is
  verified.

The similarly named RATOC RS-WSUHA-P and ROHM BP35C2 use a text-based `SK...`
command protocol and are not supported. J11 adapters use ROHM's binary UART
protocol.

## Safety and security

B-route authentication IDs and passwords are secrets. Never include real
credentials, meter identifiers, MAC addresses, PAN IDs, USB serial numbers,
captured frames, or unredacted diagnostics in source, tests, logs, exceptions,
or bug reports. Use synthetic values in fixtures and load credentials from a
secret store or the process environment at runtime.

This project communicates with a utility meter through a consumer USB radio
adapter. It does not require, authorize, or provide instructions for opening a
meter or modifying mains wiring. Do not treat readings or connection status as
an electrical-safety alarm. Installation, electrical work, and utility-meter
service must be handled by qualified parties under the rules for your location.

## Home Assistant relationship

This repository is the framework-independent protocol package. It deliberately
has no Home Assistant dependency and does not itself install a Home Assistant
integration. The package is being extracted from the separately maintained
`home-assistant-broute-j11` custom integration and is intended to support that
integration and a focused extension to Home Assistant Core's existing
`route_b_smart_meter` integration.

Home Assistant entities, config flows, diagnostics, and coordinator behavior
belong in those integration repositories rather than this package.

## Development

Python 3.11, 3.12, and 3.13 are supported. Create and activate a virtual
environment, then install the development dependencies:

```console
python -m venv .venv
python -m pip install -e ".[dev]"
```

Run the same checks used by CI:

```console
ruff format --check .
ruff check .
mypy src tests
pytest -q --cov=broute_j11 --cov-branch --cov-report=term-missing
python -m build
python -m twine check dist/*
```

Tests that need protocol traffic must use synthetic frames. Hardware checks are
opt-in and must never print or persist credentials.

## License

This project is available under the [MIT License](LICENSE).
