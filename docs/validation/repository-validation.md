# Repository Validation

This checklist ensures the repository can be cloned and used from scratch without undocumented manual steps.

## Repository
- [ ] Repository clones successfully

## Python
- [ ] Correct Python version detected
- [ ] Virtual environment created

## Dependencies
- [ ] Dependencies install successfully
- [ ] Lockfile resolves correctly

## Pre-commit
- [ ] pre-commit installs
- [ ] Hooks execute successfully

## Formatting
- [ ] Ruff passes
- [ ] Formatting check passes

## Make Commands
- [ ] make bootstrap
- [ ] make format
- [ ] make lint
- [ ] make test
- [ ] make clean

## Docker
- [ ] Images build successfully
- [ ] Containers start
- [ ] Containers stop cleanly

## Databases
- [ ] PostgreSQL reachable
- [ ] Redis reachable

## Documentation
- [ ] MkDocs builds successfully

## CI
- [ ] GitHub Actions pass

## Environment
- [ ] .env.example is complete
- [ ] No secrets committed

## Final Verification
- [ ] Fresh clone succeeds without manual fixes
- [ ] No undocumented global tool dependencies
- [ ] Bootstrap is idempotent (safe to run multiple times)
- [ ] make help lists available commands
