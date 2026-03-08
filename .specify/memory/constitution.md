<!-- 
Sync Impact Report:
- Version change: 1.0.0
- Modified principles: Initialized core principles for Simplicity, CLI Interface, Centralized Configuration, and Unified Logging.
- Added sections: Core Principles, Technical Standards, Governance
- Removed sections: N/A
- Templates requiring updates: N/A
-->
# NOVA Constitution

## Core Principles

### I. Simplicity First
Future code and features MUST be as simple as possible. Avoid over-engineering, unnecessary abstractions, and complex design patterns when a straightforward solution exists.

### II. CLI Interface
Every feature and entry point MUST be exposed via a CLI using `typer`. CLI commands MUST be intuitive and well-documented.

### III. Centralized Configuration
Environment variables MUST be read and saved under a unified `Settings` class (using `dataclasses` and `python-dotenv`) that can be imported globally. The configuration SHOULD be minimal and only contain necessary fields.

### IV. Unified Logging
Logging MUST use a unified setup with the `rich` library for console output and standard rotating files for persistence. The setup MUST provide a single `get_logger` entry point and keep third-party logs quiet.

## Technical Standards

### Minimal Application Configuration
The configuration SHOULD look something like this:

```python
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    log_level: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    log_dir: str = field(default_factory=lambda: os.getenv("LOG_DIR", "./logs"))

_settings_instance = None

def get_settings() -> Settings:
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance
```

### Minimal Logging Setup
The logging setup SHOULD look something like this:

```python
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler

def setup_unified_logging(log_level: str = "INFO", log_dir: str = "./logs"):
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    root_logger.handlers.clear()

    # Rich console handler
    console_handler = RichHandler(rich_tracebacks=True, markup=True)
    console_handler.setLevel(numeric_level)
    root_logger.addHandler(console_handler)

    # File handler
    log_file = Path(log_dir) / "app.log"
    file_handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
```

## Governance

Constitution supersedes all other practices; Amendments require documentation, approval, migration plan.
All PRs and additions MUST be reviewed against the "Simplicity First" principle. Complexity MUST be justified.

**Version**: 1.0.0 | **Ratified**: 2026-03-08 | **Last Amended**: 2026-03-08
