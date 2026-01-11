# Changelog
## [0.2.3] - 2026-01-11
### Added
- `optional` validator alias (identical behavior to `none_if_blank

## [0.2.1] - 2025-12-23
### Changed
- validate_user_option will respect q=False and ignore it correctly

## [0.2.0] - 2025-12-23
### Added
- Official custom validator extension API:
  - `register_validator`
  - `register_validators`
  - `get_validators`
  - `unregister_validator`
- Explicit public exports in `__init__.py`
- Documented case-sensitivity rules for validators
- Table of contents in README

### Changed
- Clarified and documented validator behavior (no runtime behavior changes)

## [0.1.5] - 2025-11-20
### Added
- is_valid_decimal()

## [0.1.4] - 2024-08-11
### Added
- validate_user_option_multi()
- validate_user_option_value_multi()
- retain key types in kwargs
