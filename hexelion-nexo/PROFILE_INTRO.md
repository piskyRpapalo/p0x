# EL NEXO

**This dashboard is not pretty. It is honest.**

It is 14 KiB — about what minified htmx costs before it renders anything — with zero external dependencies and a
29 MB resident footprint. It watches four machines meshed over Tailscale: a mini
PC, an ARM single-board computer, an SBC with a software-defined radio, and a
GPU module. When something breaks it tells you *which* service died and how it
knows, instead of an infinite spinner or a decorative zero.

That is the whole design. The convenient label for the failing radio node was
"SDR disconnected" — except the same antenna is receiving aircraft with
sub-second message ages, so the hardware is present and the *service* is down.
Same red light, entirely different repair. Elsewhere `systemd` reports
`Result=success` for a service that never started, which would have rendered a
never-fired timer green. Both are now `NO_DATA` with a stated cause, and both
have tests.

The numbers come from refusals. One thread reads the sensors and composes
finished HTML; Server-Sent Events push only the sections that changed; the
browser's native `EventSource` places a string and computes nothing. No React,
no htmx, no Alpine — not even vendored. No write verb, no SSH, no cloud, no
build step. 126 tests, one runner.

I build Edge systems that put the truth of the data above empty aesthetics.
