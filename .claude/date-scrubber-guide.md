# Claude Assistant Structure

## Overview

This repository uses a generic Claude workflow that can handle any development task. Task-specific knowledge is maintained in separate guide files that Claude references when needed.

## Workflow Structure

### Generic Claude Workflow (`.github/workflows/claude.yml`)
- Triggers on any `@claude` comment on any issue
- Sets up the development environment (uv, dependencies)
- No specialized prompts - Claude determines what to do based on issue content
- Claude reads issue details and any referenced guide files

### Task-Specific Guides (`.claude/` directory)
- Contains detailed instructions for specific types of tasks
- Claude references these when working on related issues
- Not user-facing documentation - internal guides for Claude

## Date Scrubber Implementation Guide

When asked to add support for new date formats to the DateScrubber:

### 1. Examine Current Implementation
Look at `approvaltests/scrubbers/date_scrubber.py:9-74` to see existing patterns:

```python
def get_supported_formats() -> List[Tuple[str, List[str]]]:
    return [
        (
            "[a-zA-Z]{3} [a-zA-Z]{3} \\d{2} \\d{2}:\\d{2}:\\d{2}",
            ["Tue May 13 16:30:00"],
        ),
        # ... more patterns
    ]
```

### 2. Create the Regex Pattern
For a new date format, create a regex pattern that matches the structure:
- Use `\\d` for digits (escape the backslash for the string)
- Use `[a-zA-Z]{3}` for 3-letter words (day/month abbreviations)  
- Use `[a-zA-Z]{3,4}` for 3-4 letter words (timezone abbreviations)
- Be specific about separators (spaces, colons, dashes, etc.)

### 3. Add to get_supported_formats()
Add your new tuple to the list:
```python
(
    "your_regex_pattern_here",
    ["Example Date String That Matches"],
),
```

### 4. Test Your Changes
```bash
# Specific date scrubber tests
uv run pytest tests/scrubbers/test_date_scrubber.py -v

# All tests  
uv run pytest tests/

# Type checking
uv run tox -e mypy
```

### Example: Adding RFC 2822 Format
For format: `Mon, 15 Jan 2024 09:30:45 GMT`

1. **Pattern**: `[a-zA-Z]{3}, \\d{2} [a-zA-Z]{3} \\d{4} \\d{2}:\\d{2}:\\d{2} [a-zA-Z]{3}`
2. **Add to list**:
   ```python
   (
       "[a-zA-Z]{3}, \\d{2} [a-zA-Z]{3} \\d{4} \\d{2}:\\d{2}:\\d{2} [a-zA-Z]{3}",
       ["Mon, 15 Jan 2024 09:30:45 GMT"],
   ),
   ```

### Reference Implementation
See PR #206 from the upstream repository:
- `gh pr view 206 --repo approvals/ApprovalTests.Python`
- `gh pr diff 206 --repo approvals/ApprovalTests.Python`

## Usage Pattern

1. Create issue describing the task
2. Comment with `@claude` and specific requirements
3. Claude reads the issue and references appropriate guide files
4. Claude implements the changes following the documented patterns