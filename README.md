# GitHub Actions Collection

![Coverage](https://byob.yarr.is/emiperez95/github-actions/coverage)
![Tests](https://github.com/emiperez95/github-actions/workflows/Test%20Coverage%20Badge%20Action/badge.svg)

A collection of reusable GitHub Actions for common development workflows.

## Available Actions

### 🛡️ Coverage Badge

Generate and update coverage badges using BYOB (Bring Your Own Badge).

**Location**: [`coverage-badge/`](./coverage-badge/)

**Usage**:
```yaml
- name: Update Coverage Badge
  uses: emiperez95/github-actions/coverage-badge@v2
  with:
    coverage-file: 'coverage.json'
```

**Features**:
- ✅ Extracts coverage from JSON reports
- 🎨 Automatic color coding based on percentage
- 📊 Uses BYOB for repository-hosted badges
- 🚀 No secrets required - uses built-in GITHUB_TOKEN
- 🛡️ Comprehensive error handling

[📖 Full Documentation](./coverage-badge/README.md)

## Usage Pattern

All actions in this repository follow a consistent pattern:

1. **Copy to your project** (for local development)
2. **Reference remotely** (for production use)
3. **Pin to specific versions** for stability

### Local Development
```yaml
uses: ./.github/actions/coverage-badge
```

### Production Use
```yaml
uses: emiperez95/github-actions/coverage-badge@v2
```

## Contributing

This repository contains actions extracted from working projects. Each action includes:

- ✅ Complete documentation
- ✅ Example usage
- ✅ Error handling
- ✅ Configurable inputs/outputs
- ✅ Real-world testing

## Repository Structure

```
github-actions/
├── README.md                    # This file
├── coverage-badge/
│   ├── action.yml              # Action definition
│   └── README.md               # Documentation
└── future-action/
    ├── action.yml
    └── README.md
```

## License

Each action may have its own license terms. See individual action directories for details.

## Roadmap

Future actions to add:
- 🚀 Auto-deployment actions
- 📝 Documentation generators
- 🔍 Code quality checks
- 📦 Package publishing workflows

---

**Note**: This repository is designed to be modular. Each action can be used independently or as part of a larger workflow.