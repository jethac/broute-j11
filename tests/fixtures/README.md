# Test fixtures

Every fixture in this directory is synthetic. Two families exist, and neither
describes a real installation:

1. **Documented golden vectors** — byte-for-byte frame samples published in
   ROHM's public B-route application note (`BP35C0-J11 B-Route Communication`,
   No. 63AN028E, §5.1–§5.4) and UART IF specification (No. 63TR008E). They use
   the documentation's placeholder authentication ID, password, MAC address,
   PAN ID, and meter readings so encoders can be checked against independent
   specification examples.
2. **Repository-invented values** — clearly synthetic credentials and meter
   properties used by `fake_adapter.py` where a test needs behavior that the
   published examples do not provide.

`frames.py` documents which command or notification each constant represents.
The repository secret scan covers this directory; new credential-shaped or
identifier-shaped data must be synthetic and documented here.
