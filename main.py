"""JOCHEN X executable entry point."""

from app.host import ApplicationHost


def main() -> int:
    """Start the desktop application and return its exit code."""
    host = ApplicationHost.create_default()
    return host.run()


if __name__ == "__main__":
    raise SystemExit(main())
