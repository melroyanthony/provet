# Test Suite for Provet

![Pytest](https://img.shields.io/badge/Pytest-8.3%2B-blue)
![Coverage](https://img.shields.io/badge/Coverage-Reports-brightgreen)
![Python](https://img.shields.io/badge/Python-3.13%2B-green)

This directory contains the comprehensive test suite for the Provet Discharge Note Generator, ensuring code quality and correctness through automated testing.

## ✨ Features

- 🧪 **Unit Tests**: Thorough testing of individual components
- 📊 **Coverage Reports**: HTML and terminal-based test coverage reporting
- 🔄 **CI Integration**: Tests run automatically in the Docker build process
- 🛡️ **Mocked Dependencies**: Tests run without external API calls
- 🧩 **Fixtures**: Reusable test components for consistent testing
- 📝 **BDD Style**: Tests follow the Given-When-Then format

## 📁 Structure

```
tests/
├── conftest.py           # Shared fixtures used across test files
├── unit/                 # All unit tests organized by module
│   ├── provet/core/      # Unit tests for core modules
│   ├── provet/utils/     # Unit tests for utility modules
│   └── api/              # Unit tests for the FastAPI endpoints
└── README.md             # This file
```

## 🚀 Running Tests

You can run tests using the provided script from the project root:

```bash
./run_tests.sh
```

Or directly with pytest:

```bash
python -m pytest
```

### Coverage Reports

Generate detailed coverage reports with:

```bash
python -m pytest --cov=provet --cov=api --cov-report=term --cov-report=html
```

This creates:
- A terminal summary of coverage statistics
- A browsable HTML report in the `htmlcov/` directory

## 🧪 Test Philosophy

Our tests follow the "Given-When-Then" format for clarity and consistency:

1. **Given**: The test setup and preconditions
   ```python
   # Example
   @pytest.fixture
   def sample_consultation():
       return {"patient": {"name": "Sparky"}, "consultation": {...}}
   ```

2. **When**: The action being tested
   ```python
   # Example
   result = generator.generate_discharge_note(sample_consultation)
   ```

3. **Then**: The expected outcomes and assertions
   ```python
   # Example
   assert "Sparky" in result.content
   assert result.format == "json"
   ```

We maximize test coverage while minimizing test code through:
- Fixtures for common test data
- Parametrization for testing multiple scenarios
- Mocks for external dependencies

## 🛡️ Mocking OpenAI

All tests that would normally call the OpenAI API use mocks to:

- ✅ Avoid incurring any API costs
- ✅ Enable testing without API credentials
- ✅ Ensure tests are fast and deterministic

The tests validate:
1. That the correct parameters are passed to the API
2. That response processing works correctly
3. That error handling functions as expected

## 📚 Related Resources

- [Main Project README](../README.md)
- [API README](../api/README.md)
- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/) 