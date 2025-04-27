# Variables
PART ?= patch  # puede sobrescribirse con: make bump-version PART=minor

# Delete the virtual environment and force a sync
venv:
	rm -rf .venv && \
	echo "✅ Deleted virtual environment" && \
	uv sync && \
	echo "✅ Created virtual environment" && \
	uvx --from=toml-cli toml get --toml-path=pyproject.toml project.version

# Bump patch/minor/major version
bump-version:
	@v=$$(uvx --from=toml-cli toml get --toml-path=pyproject.toml project.version) && \
	echo "🔧 Current version: $$v" && \
	uvx --from bump2version bumpversion --allow-dirty --current-version "$$v" $(PART) pyproject.toml && \
	echo "✅ Version bumped to new $(PART)"

# Build python package
build: bump-version
	uv build

# Clean build artifacts
clean:
	rm -rf dist *.egg-info build && \
	echo "✅ Cleaned build artifacts"

# Publish package on PyPI (use UV_PYPI_TOKEN or .pypirc for authentication)
publish: build
	uv publish

# Publish on TestPyPI
publish-test: build
	uv publish --repository testpypi

# Alias for all the Python package release cycle
release: clean build publish

# Development utilities
# Ruff lint (style, imports, common errors)
lint:
	uv run ruff check src

# Sort imports
format:
	uv run ruff format src
	uv run ruff check --fix src

# Typing with mypy
type-check:
	uv run mypy src

# Bandit security scan
security-check:
	uv run bandit -r src

# Full review
check: lint format type-check security-check


# Test execution	
test:
	uv run pytest -v --tb=short --doctest-modules --disable-warnings --maxfail=1 --junitxml=junit.xml --cov-report term-missing --cov-report html:coverage_html_report --cov-report xml:coverage.xml --cov-config=.coveragerc --cov src tests
