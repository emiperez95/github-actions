# Coverage Badge Action

![Coverage](https://byob.yarr.is/emiperez95/github-actions/coverage)
![Tests](https://github.com/emiperez95/github-actions/workflows/Test%20Coverage%20Badge%20Action/badge.svg)

A GitHub Action that automatically updates a coverage badge using BYOB (Bring Your Own Badge). This action extracts coverage data from a JSON file, determines the appropriate badge color based on coverage percentage, and updates a repository-hosted badge that displays dynamic coverage information.

**✨ No secrets required!** This action uses the built-in `GITHUB_TOKEN` and stores badge data directly in your repository.

## Testing

This action includes comprehensive tests to ensure reliability:

- **Unit Tests**: Python logic is tested with pytest
- **Integration Tests**: GitHub Actions workflow tests various scenarios
- **Local Testing**: Use `act` to test workflows locally

### Running Tests Locally

1. **Run unit tests**:
   ```bash
   cd coverage-badge
   python -m pytest tests/ -v
   ```

2. **Test with act** (requires [act](https://github.com/nektos/act) installed):
   ```bash
   ./test-local.sh
   ```

3. **Manual testing**:
   ```bash
   # Test the Python script directly
   python coverage_badge.py tests/fixtures/coverage_90.json
   ```

### Test Structure

```
coverage-badge/
├── tests/
│   ├── fixtures/           # Test coverage JSON files
│   │   ├── coverage_90.json
│   │   ├── coverage_50.json
│   │   └── invalid_coverage.json
│   └── test_coverage_badge.py  # Unit tests
├── coverage_badge.py       # Extracted Python logic
└── test-local.sh          # Local testing script
```

## Features

- ✅ Extracts coverage percentage from JSON coverage reports
- 🎨 Automatically determines badge color based on coverage thresholds
- 📊 Updates repository-hosted badge using BYOB
- 🔗 Generates BYOB-compatible badge URL
- 🚀 Configurable inputs for different project setups
- 🛡️ Comprehensive error handling

## Usage

### Basic Usage

```yaml
- name: Update Coverage Badge
  uses: emiperez95/github-actions/coverage-badge@v2
  with:
    coverage-file: 'coverage.json'
```

### Advanced Usage

```yaml
- name: Update Coverage Badge
  uses: emiperez95/github-actions/coverage-badge@v2
  with:
    coverage-file: 'coverage.json'
    badge-label: 'test coverage'
    badge-name: 'my-coverage'
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `coverage-file` | Path to the coverage JSON file | ❌ No | `coverage.json` |
| `badge-label` | Label text for the badge | ❌ No | `Coverage` |
| `badge-name` | Name identifier for the badge (used internally by BYOB) | ❌ No | `coverage` |

## Outputs

| Output | Description |
|--------|-------------|
| `coverage-percentage` | The extracted coverage percentage |
| `badge-color` | The determined badge color based on coverage |
| `badge-url` | The BYOB URL for the badge |

## Coverage Color Thresholds

The action automatically determines badge colors based on coverage percentage:

| Coverage | Color | Badge Color |
|----------|-------|-------------|
| ≥ 90% | Bright Green | ![90%](https://img.shields.io/badge/coverage-90%25-brightgreen) |
| 80-89% | Green | ![85%](https://img.shields.io/badge/coverage-85%25-green) |
| 70-79% | Yellow Green | ![75%](https://img.shields.io/badge/coverage-75%25-yellowgreen) |
| 60-69% | Yellow | ![65%](https://img.shields.io/badge/coverage-65%25-yellow) |
| 50-59% | Orange | ![55%](https://img.shields.io/badge/coverage-55%25-orange) |
| < 50% | Red | ![45%](https://img.shields.io/badge/coverage-45%25-red) |

## Setup Requirements

### 1. Coverage JSON File

Your CI workflow must generate a coverage report in JSON format. For pytest, use:

```yaml
- name: Run tests with coverage
  run: pytest --cov=src --cov-report=json
```

The JSON file should have the structure:
```json
{
  "totals": {
    "percent_covered_display": "85.2"
  }
}
```

### 2. Repository Permissions

**⚠️ CRITICAL**: Your workflow MUST have write permissions for BYOB to work:

```yaml
permissions:
  contents: write
```

Without this permission, the action will fail with a "Permission denied" error.

### 3. README Badge

Add the badge to your README.md:

```markdown
![Coverage](https://byob.yarr.is/YOUR_USERNAME/YOUR_REPO_NAME/coverage)
```

Replace `coverage` with your `badge-name` if you used a custom name.

### 4. No Additional Setup Required

The coverage badge uses BYOB (Bring Your Own Badge) which stores badge data in the repository itself using the built-in `GITHUB_TOKEN`. No personal access tokens, gists, or external services are required!

## Example Workflow

```yaml
name: Tests
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

permissions:
  contents: write

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install pytest pytest-cov
    
    - name: Run tests
      run: pytest --cov=src --cov-report=json
    
    - name: Update Coverage Badge
      if: github.ref == 'refs/heads/main' && github.event_name == 'push'
      uses: emiperez95/github-actions/coverage-badge@v2
      with:
        coverage-file: 'coverage.json'
```

## Error Handling

The action includes comprehensive error handling:

- **Missing coverage file**: Clear error message with file path
- **Invalid JSON structure**: Helpful error about expected format
- **Badge update failures**: Detailed error messages from BYOB action
- **Missing inputs**: Validation of required parameters

## Troubleshooting

### Badge shows "invalid" or doesn't appear
- Ensure the workflow has run at least once on the main branch
- Check that the BYOB action completed successfully in Actions tab
- Verify the badge URL uses correct username/repository name

### Coverage not updating
- Verify the coverage file path is correct
- Check that the JSON structure matches expectations
- Review the action logs for error messages

### Permission denied errors
- No longer applicable! BYOB uses the built-in GITHUB_TOKEN

## Migration from Inline Scripts

If you're migrating from inline coverage scripts:

1. Replace the coverage extraction and gist update steps with this action
2. Move hardcoded values to inputs
3. Update any references to step outputs (they may have changed names)

## Future Enhancements

This action is designed to be easily extractable to a shared repository for reuse across multiple projects. The modular design makes it simple to:

- Move to a separate repository
- Publish to GitHub Marketplace
- Share across organizations
- Version independently

## License

This action is part of the github-actions repository and follows the same license terms.