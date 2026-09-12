import logging
import json
import sys

class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "timestamp": self.formatTime(record),
            "extra_payload": getattr(record, "extra_payload", None)
        }, default=str)

def setup_logging(level=logging.INFO):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    root = logging.getLogger()
    root.handlers = []  # avoid duplicate handlers on reload
    root.addHandler(handler)
    root.setLevel(level)