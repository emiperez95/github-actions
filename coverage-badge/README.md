# Coverage Badge Gist Action

A GitHub Action that automatically updates a coverage badge using GitHub Gist and shields.io. This action extracts coverage data from a JSON file, determines the appropriate badge color based on coverage percentage, and updates a GitHub Gist that can be used with shields.io to display a dynamic coverage badge.

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
- 📊 Updates GitHub Gist with badge data
- 🔗 Generates shields.io compatible badge URL
- 🚀 Configurable inputs for different project setups
- 🛡️ Comprehensive error handling

## Usage

### Basic Usage

```yaml
- name: Update Coverage Badge
  uses: ./.github/actions/coverage-badge
  with:
    gist-id: 'your-gist-id-here'
    gist-token: ${{ secrets.GIST_SECRET }}
```

### Advanced Usage

```yaml
- name: Update Coverage Badge
  uses: ./.github/actions/coverage-badge
  with:
    gist-id: 'your-gist-id-here'
    gist-token: ${{ secrets.GIST_SECRET }}
    coverage-file: 'coverage.json'
    gist-filename: 'my-project-coverage.json'
    badge-label: 'test coverage'
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `gist-id` | GitHub Gist ID where badge data will be stored | ✅ Yes | - |
| `gist-token` | GitHub Personal Access Token with gist scope | ✅ Yes | - |
| `coverage-file` | Path to the coverage JSON file | ❌ No | `coverage.json` |
| `gist-filename` | Filename to use in the Gist | ❌ No | `coverage.json` |
| `badge-label` | Label text for the badge | ❌ No | `coverage` |
| `dry-run` | Skip gist update for testing (true/false) | ❌ No | `false` |

## Outputs

| Output | Description |
|--------|-------------|
| `coverage-percentage` | The extracted coverage percentage |
| `badge-color` | The determined badge color based on coverage |
| `badge-url` | The complete shields.io URL for the badge |

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

### 2. GitHub Gist

1. Create a new gist at https://gist.github.com
2. Use any filename (e.g., `coverage.json`)
3. Add initial content:
   ```json
   {
     "schemaVersion": 1,
     "label": "coverage",
     "message": "0%",
     "color": "red"
   }
   ```
4. Copy the Gist ID from the URL

### 3. GitHub Personal Access Token

1. Go to https://github.com/settings/tokens
2. Create a new token with `gist` scope
3. Add it as a repository secret named `GIST_SECRET`

### 4. README Badge

Add the badge to your README.md:

```markdown
![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/USERNAME/GIST_ID/raw/FILENAME.json)
```

## Example Workflow

```yaml
name: Tests
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

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
      uses: ./.github/actions/coverage-badge
      with:
        gist-id: 'your-gist-id-here'
        gist-token: ${{ secrets.GIST_SECRET }}
```

## Error Handling

The action includes comprehensive error handling:

- **Missing coverage file**: Clear error message with file path
- **Invalid JSON structure**: Helpful error about expected format
- **Gist update failures**: Detailed error messages from GitHub API
- **Missing inputs**: Validation of required parameters

## Troubleshooting

### Badge shows "invalid"
- Check that the Gist ID is correct
- Verify the GIST_SECRET has proper permissions
- Ensure the workflow has run at least once

### Coverage not updating
- Verify the coverage file path is correct
- Check that the JSON structure matches expectations
- Review the action logs for error messages

### Permission denied errors
- Ensure GIST_SECRET has `gist` scope
- Check that the token hasn't expired

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

This action is part of the video-processing-pipeline project and follows the same license terms.