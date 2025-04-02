# Running GitHub Workflows Locally

This document explains how to run GitHub Actions workflows locally to test them before pushing changes to the repository.

## Prerequisites

1. **Docker**: Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. **Act**: Install the [nektos/act](https://github.com/nektos/act) tool
   - MacOS: `brew install act`
   - Linux: `curl -s https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash`
   - Windows: `choco install act-cli` or download from GitHub releases

## Using the Helper Script

We've created a helper script to make running workflows locally easier:

```bash
# Make the script executable if needed
chmod +x scripts/run-workflow-locally.sh

# List available workflows
./scripts/run-workflow-locally.sh --list

# Run the tests workflow (just the tests)
./scripts/run-workflow-locally.sh -j test .github/workflows/tests.yml

# Run the CI/CD workflow (the full pipeline)
./scripts/run-workflow-locally.sh .github/workflows/ci-cd.yml

# Run a workflow with a specific event type
./scripts/run-workflow-locally.sh -e pull_request .github/workflows/ci-cd.yml
```

## Common Options

- `-h, --help`: Show help message
- `-l, --list`: List available workflows
- `-j, --job JOB`: Run a specific job in the workflow
- `-e, --event TYPE`: Specify the event type (push, pull_request)

## Tips for Running Workflows Locally

1. **GitHub Secrets**: For workflows that require secrets, create a `.secrets` file:
   ```
   GITHUB_TOKEN=your_token_here
   ```

2. **Limited Resources**: Some workflows might require more resources than available locally:
   ```bash
   # Run with larger memory allocation
   act -m
   ```

3. **GitHub API Limitations**: Some actions that interact with GitHub API might not work locally.

4. **Common Issues**:
   - If Docker runs out of memory, increase the allocation in Docker Desktop settings
   - Use `-P ubuntu-latest=catthehacker/ubuntu:act-latest` for better OS compatibility

## Modifying Workflows for Local Testing

You may need to make small adjustments for local testing:

1. **GitHub Pages deployment**: This won't work locally but will be skipped
2. **Matrix builds**: These might take longer locally
3. **GitHub-specific actions**: Some may need to be mocked or skipped

## Comparing Results

After running a workflow locally, check the following:

1. Test results and coverage reports in the `.act-artifacts` directory
2. Error messages and logs in the console output
3. Container behavior differences

## Troubleshooting

If you encounter issues:

1. **Permissions Problems**: Check that Docker has sufficient permissions
2. **Missing Dependencies**: Make sure all required tools are installed
3. **Version Mismatches**: Verify Docker, Act, and dependencies are up to date 