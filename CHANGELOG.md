# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-11-21

### Added
- **Build System**: Added `Makefile` to automate cross-platform compilation (Windows, Mac, Linux) using `fyne-cross`.
- **Distribution**: Builds are now organized in a `Releases/` directory.
- **Assets**: Added application icon (`Icon.png`) to executables.
- **Documentation**: Added comprehensive English comments to `main.go` to explain UI and scraping logic.

### Changed
- Updated `.gitignore` to exclude build artifacts and release folders.
- Updated `README.md` with detailed build and installation instructions.

## [1.0.0] - 2025-11-21

### Added
- **Go Implementation**: Complete rewrite of the application using Go.
- **GUI**: Native-looking cross-platform GUI using [Fyne](https://fyne.io/).
- **Scraper**: Improved scraping logic using [Chromedp](https://github.com/chromedp/chromedp) (Chrome DevTools Protocol) instead of Selenium.
- **Project Structure**: Standard Go project layout.
- MIT License.

### Changed
- **Performance**: Significantly improved performance and reduced runtime dependencies compared to the Python version.
- **Build System**: Switched to `go build` for easier cross-platform compilation.
- Updated `README.md` with new installation and usage instructions.

### Removed
- Legacy Python implementation (`main.py`).
- `requirements.txt` and Python dependencies (Selenium, CustomTkinter).

## [0.1.0] - 2025-11-21

### Added
- Initial release (Python).
- Basic GUI using CustomTkinter.
- Facebook image downloading logic using Selenium WebDriver.
