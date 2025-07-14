# Contributing to GitHub Actions Collection

Thank you for your interest in contributing to this collection of GitHub Actions!

## Development Setup

### Prerequisites

- Python 3.8+
- pytest (for testing)
- act (optional, for local workflow testing)
- Docker (required for act)

### Installing Dependencies

```bash
# Install Python test dependencies
pip install pytest pytest-cov

# Install act (macOS)
brew install act

# Install act (Windows)
choco install act-cli
```

## Testing

### Running Tests

Each action in this repository includes its own test suite:

```bash
# Run unit tests for an action
cd coverage-badge
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=. --cov-report=term-missing

# Test locally with act
./test-local.sh
```

### Test Structure

Each action should have:
- `tests/` directory with unit tests
- `tests/fixtures/` with test data
- Integration tests in `.github/workflows/`
- Local test scripts where appropriate

### Writing Tests

1. **Unit Tests**: Test individual functions and logic
2. **Integration Tests**: Test the action in a workflow
3. **Error Cases**: Test error handling and edge cases

## Adding New Actions

1. Create a new directory for your action
2. Include:
   - `action.yml` - Action definition
   - `README.md` - Documentation
   - `tests/` - Test suite
   - Any supporting scripts

3. Follow the existing patterns for:
   - Input/output definitions
   - Error handling
   - Documentation

## Code Style

- Use clear, descriptive names
- Add comments for complex logic
- Follow existing patterns in the codebase
- Include comprehensive error messages

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Add tests for your changes
4. Ensure all tests pass
5. Update documentation
6. Submit a pull request

## Testing Checklist

Before submitting a PR:

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Documentation is updated
- [ ] Action works with `act` locally
- [ ] Error cases are handled
- [ ] Inputs are validated

## Security Considerations

- Never commit secrets or credentials
- Use GitHub secrets for sensitive data
- Validate all inputs
- Follow GitHub Actions security best practices

## Questions?

Open an issue for:
- Bug reports
- Feature requests
- Questions about contributing

Thank you for helping improve this action collection!