import logging
import sys

from toying_with_mcp_features.config import SERVER_LOG_FILE, ENV_TYPE

# Set some new handlers and formatters for FastMCP server
# As FastMCP implements a middleware logger, we modify it here to fit the project needs

log_level = logging.WARNING
if ENV_TYPE == "dev" and SERVER_LOG_FILE.exists():
    log_level = logging.DEBUG


# --- Correct Logging Configuration ---
root_logger = logging.getLogger()

formatter = logging.Formatter(
    fmt="[%(asctime)s] %(levelname)s\t%(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
)

# Console handler
console_handler = logging.StreamHandler(stream=sys.stderr)
console_handler.setLevel(logging.INFO)  # What appears in the client notifications
console_handler.setFormatter(formatter)
root_logger.addHandler(console_handler)

# File handler
SERVER_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
file_handler = logging.FileHandler(filename=SERVER_LOG_FILE, mode="a")
file_handler.setLevel(log_level)
file_handler.setFormatter(formatter)
root_logger.addHandler(file_handler)

# Set the overall root logger level to DEBUG
root_logger.setLevel(log_level)