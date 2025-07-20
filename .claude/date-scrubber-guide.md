# Adding formats to Date Scrubber

## Reference Implementation

Important! Before anything else, first see PR #206 from the upstream repository, you should have permissions for that:

- `gh pr view 206 --repo approvals/ApprovalTests.Python`
- `gh pr diff 206 --repo approvals/ApprovalTests.Python`

## Test 

```bash
uv run pytest tests/scrubbers/test_date_scrubber.py -v
uv run pytest tests/
```
