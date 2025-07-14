#!/bin/bash
# Local testing script for the coverage badge action

set -e

echo "🧪 Testing Coverage Badge Action Locally"
echo "========================================"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test the Python script directly
echo -e "\n📊 Testing Python script..."
python coverage_badge.py tests/fixtures/coverage_90.json test-gist test.json

# Run unit tests
echo -e "\n🔬 Running unit tests..."
python -m pytest tests/ -v

# Create a test workflow for act
echo -e "\n🎭 Creating test workflow for act..."
cat > .github/workflows/test-local.yml << 'EOF'
name: Test Coverage Badge Locally
on: push

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Create test coverage file
        run: |
          cat > coverage.json << 'JSON'
          {
            "totals": {
              "percent_covered_display": "87.5"
            }
          }
          JSON
      
      - name: Test action with dry-run
        id: test-action
        uses: ./coverage-badge
        with:
          gist-id: 'test-gist-id'
          gist-token: 'test-token'
          coverage-file: coverage.json
          dry-run: 'true'
      
      - name: Display results
        run: |
          echo "Coverage: ${{ steps.test-action.outputs.coverage-percentage }}%"
          echo "Color: ${{ steps.test-action.outputs.badge-color }}"
          echo "Badge URL: ${{ steps.test-action.outputs.badge-url }}"
EOF

# Run with act if available
if command -v act &> /dev/null; then
    echo -e "\n🚀 Running workflow with act..."
    cd ..
    act -W .github/workflows/test-local.yml --container-architecture linux/amd64
    cd coverage-badge
else
    echo -e "\n⚠️  act is not installed. Install it with:"
    echo "    brew install act  # macOS"
    echo "    choco install act-cli  # Windows"
    echo ""
    echo "Then run this script again to test with act."
fi

# Clean up
rm -f ../.github/workflows/test-local.yml

echo -e "\n${GREEN}✅ Testing complete!${NC}"