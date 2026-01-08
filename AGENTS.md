## Build/Lint/Test Commands

- **Build**: Run `python -m unittest discover -s tests`
- **Lint**: Run `flake8 .`
- **Test**: Run `python -m unittest test_name`

## Code Style Guidelines

### Imports
- Use absolute imports
- Sort imports into the following categories: Standard library, Related third party, Local application/library specific
- Put a blank line between these categories

### Formatting
- Use 4 spaces for indentation
- Limit line length to 79 characters
- Use blank lines to separate functions and classes

### Types
- Use type hints where appropriate
- Import types from `typing` module

### Naming Conventions
- Use `lowercase_with_underscores` for function and variable names
- Use `CamelCase` for class names
- Use `ALL_UPPERCASE` for constants

### Error Handling
- Catch specific exceptions rather than generic exceptions
- Use `finally` to ensure cleanup code runs regardless of exceptions
- Log exceptions with `logging` module

## Cursor Rules

- Ensure all imports are at the top of the file
- Use type hints for function parameters and return values
- Keep function and class definitions small and focused

## Copilot Rules

- Use descriptive commit messages
- Ensure all code is tested before committing
- Follow the code style guidelines when modifying existing code
