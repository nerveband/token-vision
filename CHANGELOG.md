# Changelog

All notable changes to Token Vision will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-02

### Added
- Initial release of Token Vision
- Core token calculation functionality for images
- Support for multiple AI models:
  - Claude (Sonnet, Haiku, Opus)
  - GPT-4o (Latest, Nov 2024, Aug 2024, May 2024)
  - Gemini (Pro, Flash)
- Custom model configuration support
- Batch processing capabilities
- Cost calculation with support for:
  - Standard rates
  - Batch processing rates
  - Cached input rates
- Comprehensive documentation and examples
- Type hints and docstrings
- Development tools configuration (black, isort, mypy, ruff)
- MIT License

### Changed
- Renamed package from "image-token-calculator" to "token-vision"
- Updated model configurations to match latest pricing
- Improved token calculation accuracy

### Removed
- GPT-4V model (replaced with GPT-4o) 