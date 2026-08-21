---
name: test-quality
description: Reviews test code for meaningful behavioral coverage — detects trivial assertions, mock-everything patterns, missing edge cases, and coverage-padding. Load when reviewing pull requests containing test files, writing tests, or planning test strategy. Designed for use by review, build, and plan agents.
---

# Test Quality

Reviews whether tests actually verify meaningful behavior, not just pass. Designed to catch the common AI anti-pattern: many tests that look good but don't find real bugs.

## Anti-Pattern Detection

Check each changed or new test file against these anti-patterns:

### Trivial Assertions
- [ ] `assert True` / `assert False` — always passes, tests nothing
- [ ] `assert result is not None` without further assertions on the value
- [ ] `assert len(results) > 0` without checking content
- [ ] Assertions that duplicate what the setup/fixture already guarantees (e.g., fixture sets `name="test"`, test asserts `name == "test"`)
- [ ] No assertion at all — test body has only setup, mocks, or no-ops

### Mock-Everything Pattern
- [ ] Every external dependency mocked, no path exercises real integration
- [ ] Mocked function returns a hardcoded value that makes the assertion trivially pass
- [ ] Mocked database/API returns a perfect response — no error paths tested
- [ ] Critical business logic is inside a mocked module, so the test covers only a thin shell

### Missing Edge Cases
- [ ] No test for `None`, `null`, or empty input
- [ ] No test for boundary values (0, max, min, empty string, empty list)
- [ ] No test for error paths (exception thrown, timeout, network failure, auth denied)
- [ ] No test for duplicate/conflicting data
- [ ] No test for concurrent access or race conditions (when relevant)

### Coverage Padding
- [ ] High line coverage but trivial logic — many tests for getters, setters, constructors
- [ ] 5+ tests for a single simple function where 1-2 would suffice
- [ ] Test file is significantly larger than the implementation file but tests only surface behavior
- [ ] Every public method has a test but none test interactions between methods

### Implementation Detail Tests
- [ ] Tests reference private/internal functions (prefixed with `_`, `__`, or `private`)
- [ ] Tests assert on internal state rather than observable behavior
- [ ] Test breaks on refactoring that doesn't change behavior
- [ ] Testing that a specific mock was called — instead of testing the resulting behavior

### Shallow Seam Tests
- [ ] Regression test for a real bug exercises only a single-caller path when the bug requires multi-caller interaction
- [ ] Unit test mocks away the layer where the actual failure hides, giving false confidence
- [ ] Test asserts on intermediate state rather than the end-to-end behavioral seam
- [ ] Test setup bypasses the real entry point the bug was reached through

## Test-Relevanz-Check

For each changed function/class in the implementation diff, identify the corresponding tests. Then evaluate:

1. **Does the test exercise the critical behavior?**
   - The function handles a complex transformation → test verifies the output
   - The function reads from a database → test verifies the query + response handling
   - The function calls an API → test verifies error handling, retries, and data transformation

2. **Does the test cover realistic scenarios?**
   - Not just the happy path — what are the real failure modes?
   - Not just a single input — what are the input variations?

3. **Does the test find real bugs?**
   - If a dev introduced a subtle logic error, would this test catch it? If no: flag as weak coverage.
   - Count of "would catch" vs "would miss" scenarios.

## Review Flow

### For auto-review: When tests are in the diff

1. Collect all modified and new test files from the diff
2. Check each test function against the Anti-Pattern Detection checklist
3. Run the Test-Relevanz-Check for the corresponding implementation changes
4. Report findings:

```md
Test Quality Notes
- Coverage: <list of anti-patterns found, with file:line refs>
- [Critical] file:line — trivial test that asserts nothing real → add meaningful assertions
- [High] file:line — mock-everything, no error path tested → add integration test
- [Medium] file:line — missing edge case (None input) → add test
```

### For build: When writing new tests

1. Before writing: review the implementation to identify critical paths and edge cases
2. Write tests that cover: happy path, error path, empty/null input, boundary values
3. After writing: self-check against Anti-Pattern Detection
4. Do not submit tests that trigger any of the anti-patterns

### For plan: When discussing test strategy

1. Identify which parts of the system have the highest risk of failure (complex transformations, error handling, external integrations)
2. Recommend targeted tests for identified risks — not blanket coverage
3. Set quality gates: no trivial assertions, at least one meaningful test per identified risk
4. Explicitly state when no new test is justified (low-risk change, existing coverage sufficient)
5. Use the project's delivery profile to determine baseline: quick/standard may have no tests; production/published require risk-based coverage

## Common Anti-Pattern Examples

### Bad: Trivial Assertion
```python
# This test always passes — it only checks the fixture value
def test_user_name():
    user = UserFactory(name="Alice")
    assert user.name == "Alice"
```

### Good: Meaningful Behavior
```python
# This test checks actual behavior
def test_user_name_change_propagates():
    user = UserFactory(name="Alice")
    user.change_name("Bob")
    assert user.name == "Bob"
    # Also check that a notification was created
    assert Notification.objects.filter(user=user, event="name_change").exists()
```

### Bad: Mock-Everything
```python
@patch("myapp.services.stripe")
def test_payment(self, mock_stripe):
    mock_stripe.Charge.create.return_value = {"status": "succeeded"}
    # Everything is mocked, nothing real is tested
    result = process_payment(100)
    assert result["status"] == "succeeded"
```

### Good: Realistic Test
```python
def test_payment_failure_logged():
    """Test that payment failures are properly logged and handled."""
    # Use a test gateway or real integration test
    result = process_payment(999999)  # known-failing amount
    assert result["status"] == "failed"
    assert Log.objects.filter(event="payment_failure").exists()
```

### Bad: No Edge Cases
```python
def test_divide():
    assert divide(10, 2) == 5
```

### Good: Edge Cases Covered
```python
def test_divide_happy_path():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_divide_with_negative():
    assert divide(-10, 2) == -5
    assert divide(10, -2) == -5

def test_divide_floor():
    assert divide(10, 3) == 3  # if integer division
```

## Severity Ratings

- **Critical** — test that cannot find bugs (no meaningful assertions, always-pass, setup-only)
- **High** — significant blind spot (no error path testing, zero edge cases, mock-everything)
- **Medium** — missing coverage for important scenarios (missing boundary check, missing failure mode)
- **Low** — minor gaps (missing one trivial edge case, slightly brittle mock setup)
