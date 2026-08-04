import logging

def configure_logging(level: int = logging.INFO) -> None:
    """Configure root logging for the application.

    Call this once, at process startup, from each entrypoint
    (main.py, run_backend.py, api/main.py) before doing anything else.
    Modules elsewhere should just do `logging.getLogger(__name__)` and
    log through that — they should never call basicConfig themselves.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )