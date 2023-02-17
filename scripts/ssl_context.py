"""Provides a function for creating an appropriate SSL context."""
import ssl
import sys
import datetime
import logging

PchumLog = logging.getLogger("pchumLogger")

try:
    import certifi
except ImportError:
    if sys.platform == "darwin":
        # Certifi is required to validate certificates on MacOS with pyinstaller builds.
        PchumLog.warning(
            "Failed to import certifi, which is recommended on MacOS. "
            "Pesterchum might not be able to validate certificates unless "
            "Python's root certs are installed."
        )
    else:
        PchumLog.info(
            "Failed to import certifi, Pesterchum will not be able to validate "
            "certificates if the system-provided root certificates are invalid."
        )


def get_ssl_context():
    """Returns an SSL context for connecting over SSL/TLS.
    Loads the certifi root certificate bundle if the certifi module is less
    than a year old or if the system certificate store is empty.

    The cert store on Windows also seems to have issues, so it's better
    to use the certifi provided bundle assuming it's a recent version.

    On MacOS the system cert store is usually empty, as Python does not use
    the system provided ones, instead relying on a bundle installed with the
    python installer."""
    default_context = ssl.create_default_context()
    if "certifi" not in globals():
        return default_context

    # Get age of certifi module
    certifi_date = datetime.datetime.strptime(certifi.__version__, "%Y.%m.%d")
    current_date = datetime.datetime.now()
    certifi_age = current_date - certifi_date

    empty_cert_store = list(default_context.cert_store_stats().values()).count(0) == 3
    # 31557600 seconds is approximately 1 year
    if empty_cert_store or certifi_age.total_seconds() <= 31557600:
        PchumLog.info("Using SSL/TLS context with certifi-provided root certificates.")
        return ssl.create_default_context(cafile=certifi.where())
    PchumLog.info("Using SSL/TLS context with system-provided root certificates.")
    return default_context
