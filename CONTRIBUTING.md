# Contributing to SM Analytics

Thank you for your interest in contributing to **SM Analytics**.

This project aims to become a production-grade stock market analytics platform. Every contribution should improve the project's correctness, maintainability, scalability, and long-term quality.

This document outlines the contribution process and development expectations.

---

# Code of Conduct

By participating in this project, you agree to:

- Be respectful and professional.
- Provide constructive feedback.
- Focus discussions on technical merit.
- Welcome new contributors.

---

# Before You Contribute

Before starting work:

1. Check existing Issues and Discussions.
2. Verify that your contribution aligns with the project roadmap.
3. Open an issue for large features or architectural changes before implementation.
4. Wait for discussion if the proposal affects public APIs or architecture.

---

# Development Workflow

1. Fork the repository.
2. Create a feature branch.

```bash
git checkout -b feature/my-feature
```

3. Make changes.
4. Write or update tests.
5. Update documentation if necessary.
6. Ensure all checks pass.
7. Commit using clear commit messages.
8. Push your branch.
9. Open a Pull Request.

---

# Coding Standards

Contributors are expected to:

- Write clean, readable code.
- Prefer simplicity over cleverness.
- Follow the project's formatting and linting rules.
- Avoid unnecessary dependencies.
- Keep functions and modules focused.
- Write meaningful comments only where necessary.
- Remove dead code before submitting.

---

# Documentation

Documentation is part of the codebase.

When introducing new functionality:

- Update relevant documentation.
- Explain architectural decisions where appropriate.
- Keep examples accurate and up to date.

---

# Testing

Every contribution should include appropriate testing.

Depending on the change, this may include:

- Unit tests
- Integration tests
- End-to-end tests
- Performance tests

A Pull Request should not reduce overall project quality or test coverage.

---

# Commit Messages

Use clear and descriptive commit messages.

Examples:

```text
feat: add market data ingestion service

fix: correct Redis cache expiration

docs: update repository structure

refactor: simplify screening engine
```

---

# Pull Requests

A Pull Request should:

- Address a single logical change.
- Include a clear description.
- Reference related issues where applicable.
- Pass all automated checks.
- Be ready for code review.

Large changes should be split into multiple smaller Pull Requests whenever practical.

---

# Code Review

All submissions are reviewed before merging.

Reviews focus on:

- Correctness
- Architecture
- Maintainability
- Performance
- Security
- Testing
- Documentation

Requested changes should be addressed before approval.

---

# Reporting Issues

When reporting bugs, include:

- Environment
- Steps to reproduce
- Expected behavior
- Actual behavior
- Relevant logs or screenshots
- Version information (if applicable)

---

# Feature Requests

Feature requests should include:

- Problem statement
- Proposed solution
- Alternative approaches considered
- Expected impact
- Possible drawbacks

---

# Questions

For questions or design discussions, use the project's Discussions section or open an Issue.

---

Thank you for helping improve SM Analytics.
