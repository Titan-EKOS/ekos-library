"""Entry point used by every MCP client config. Works from any working directory."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from library_server.server import main  # noqa: E402

if __name__ == "__main__":
    main()
