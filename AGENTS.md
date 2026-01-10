# Agent Development Guide

This guide provides essential information for AI coding agents working on the simplechores Home Assistant custom integration.

## Project Overview

**simplechores** is a Home Assistant custom integration template based on integration_blueprint. It's a Python 3.13 project that follows Home Assistant core development standards.

- **Domain:** `simplechores`
- **Framework:** Home Assistant (v2025.12.5)
- **Linter/Formatter:** Ruff (v0.14.10)
- **Supported Platforms:** Sensor, Binary Sensor, Switch
- **Config Flow:** UI-based configuration enabled

## Development Commands

### Setup & Installation
```bash
# Install dependencies
python3 -m pip install -r requirements.txt

# Or use the setup script
./scripts/setup
```

### Development Server
```bash
# Start Home Assistant in debug mode with this integration
./scripts/develop

# Access at: http://localhost:8123
```

### Linting & Formatting
```bash
# Format and fix all issues (recommended)
./scripts/lint

# Or run manually:
ruff format .                    # Format code
ruff check . --fix               # Lint and auto-fix
ruff check .                     # Lint only (no fixes)
ruff format . --check            # Check formatting without changes
```

### Testing & Validation
```bash
# No unit tests currently - this is a template project

# Validate integration manifest and structure
# (Runs in CI via GitHub Actions)
# - hassfest: Validates Home Assistant integration structure
# - HACS: Validates HACS compatibility
```

### Manual Testing
Start the development server and:
1. Navigate to http://localhost:8123
2. Go to Settings → Devices & Services
3. Click "Add Integration"
4. Search for "simplechores"
5. Test configuration flow and entity functionality

## Code Style Guidelines

### Import Organization
```python
"""Module docstring."""
from __future__ import annotations  # Always first after docstring

from datetime import timedelta      # Standard library
from typing import TYPE_CHECKING    # Typing imports

from homeassistant.const import Platform  # Home Assistant imports

from .const import DOMAIN, LOGGER   # Local imports
from .data import IntegrationBlueprintData
```

**Import Rules:**
1. Start with `from __future__ import annotations`
2. Group: stdlib → typing → third-party → homeassistant → local
3. Use `TYPE_CHECKING` guard for type-only imports to avoid circular dependencies
4. Alphabetize within groups

### Type Hints & Typing
```python
# Modern Python 3.12+ type syntax
type IntegrationBlueprintConfigEntry = ConfigEntry[IntegrationBlueprintData]

# Always use type hints for function signatures
async def async_setup_entry(
    hass: HomeAssistant,
    entry: IntegrationBlueprintConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    ...

# Use TYPE_CHECKING to avoid runtime import overhead
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

# Property return types
@property
def native_value(self) -> str | None:
    """Return the native value of the sensor."""
    return self.coordinator.data.get("value")
```

**Typing Rules:**
- Always include type hints for parameters and return values
- Use `| None` for optional types (not `Optional[T]`)
- Use modern type alias syntax: `type MyType = ...`
- Leverage `TYPE_CHECKING` for type-only imports

### Naming Conventions
```python
# Constants: UPPERCASE_WITH_UNDERSCORES
DOMAIN = "simplechores"
LOGGER: Logger = getLogger(__package__)

# Classes: PascalCase
class IntegrationBlueprintEntity(CoordinatorEntity):
    ...

# Functions/methods: snake_case
async def async_setup_entry(hass: HomeAssistant) -> bool:
    ...

# Private attributes/methods: _leading_underscore
def _async_update_data(self) -> Any:
    ...

# Protected attributes (Home Assistant convention): _attr_*
_attr_attribution = ATTRIBUTION
_attr_unique_id = "unique_id_here"
```

### Docstrings
```python
"""Short one-line summary.

Longer description if needed. Follows Google style docstrings.

Args:
    hass: Home Assistant instance.
    entry: Config entry.

Returns:
    True if setup was successful.
"""
```

**Docstring Rules:**
- Every module, class, and public function must have a docstring
- Use triple double-quotes `"""`
- Keep first line short and imperative (e.g., "Set up the sensor platform.")
- Home Assistant prefers concise docstrings over verbose ones

### Formatting
- **Indentation:** 4 spaces (no tabs)
- **Line Length:** Ruff default (88 characters for formatting, 120 for linting)
- **String Quotes:** Double quotes `"` preferred (Ruff default)
- **Trailing Commas:** Used in multi-line structures

### Error Handling
```python
from homeassistant.exceptions import ConfigEntryNotReady

# Raise specific exceptions during setup
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from config entry."""
    try:
        # Setup code
        ...
    except SomeAPIException as exception:
        raise ConfigEntryNotReady from exception

# Use LOGGER for diagnostics
LOGGER.error("Failed to connect: %s", error)
LOGGER.debug("Received data: %s", data)
```

**Error Handling Rules:**
- Use specific Home Assistant exceptions (`ConfigEntryNotReady`, `ConfigEntryAuthFailed`, etc.)
- Always chain exceptions with `from` for proper tracebacks
- Log errors with appropriate levels (debug, info, warning, error)
- Use package-level `LOGGER` from `const.py`

### Async Patterns
```python
# Async functions for Home Assistant
async def async_setup_entry(...) -> bool:
    """Set up entry."""
    ...

# Coordinator updates
async def _async_update_data(self) -> Any:
    """Fetch data from API."""
    return await self.api.async_get_data()

# Entity state updates via properties (synchronous)
@property
def native_value(self) -> str | None:
    """Return sensor value."""
    return self.coordinator.data.get("value")
```

**Async Rules:**
- Use `async def` for all I/O operations
- Platform setup functions must be async
- Entity properties are synchronous (no async)
- Use `await` for all async calls (never block)

## Architecture Patterns

### Coordinator Pattern
All data fetching should use the DataUpdateCoordinator:
```python
coordinator = BlueprintDataUpdateCoordinator(
    hass=hass,
    logger=LOGGER,
    name=DOMAIN,
    update_interval=timedelta(hours=1),
)
```

### Entity Base Class
Extend `IntegrationBlueprintEntity` for all entities:
```python
class IntegrationBlueprintSensor(IntegrationBlueprintEntity, SensorEntity):
    """Sensor implementation."""
    ...
```

### Config Flow
UI configuration is handled in `config_flow.py` - always prefer config flow over YAML configuration.

## File Structure
```
custom_components/simplechores/
├── __init__.py          # Setup, entry point, platform forwarding
├── config_flow.py       # UI configuration flow
├── const.py             # Constants and domain
├── coordinator.py       # Data update coordinator
├── data.py              # Type definitions and data classes
├── entity.py            # Base entity class
├── sensor.py            # Sensor platform
├── binary_sensor.py     # Binary sensor platform
├── switch.py            # Switch platform
└── translations/        # Translation files
    └── en.json
```

## Ruff Configuration

The project uses Ruff with Home Assistant core settings:
- **Target:** Python 3.13
- **Rules:** ALL (comprehensive)
- **Max Complexity:** 25
- **Ignored Rules:** ANN401, D203, D212, COM812, ISC001

## CI/CD

GitHub Actions automatically run on PRs and commits to main:
- **Lint:** Ruff formatting and linting checks
- **Validate:** Hassfest and HACS validation

Always ensure `./scripts/lint` passes before committing.

## Additional Notes

- This is a **template/blueprint project** - placeholder code exists intentionally
- No unit tests currently configured (integration testing via manual testing)
- HACS compatible - maintain `hacs.json` and `manifest.json` properly
- Follow Home Assistant developer documentation: https://developers.home-assistant.io/
- The dev container is pre-configured for VS Code with all necessary extensions

## Resources

- [Home Assistant Developer Docs](https://developers.home-assistant.io/)
- [Integration Blueprint Template](https://github.com/ludeeus/integration_blueprint)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Home Assistant Core Style](https://github.com/home-assistant/core/blob/dev/pyproject.toml)
