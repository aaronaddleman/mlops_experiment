# ML Agent Experiment

[![Agent Coverage](https://github.com/mlops_experiment/blob/main/.github/badges/coverage-agent.svg)](https://mlops_experiment.github.io/coverage-reports/agent/)
[![UI Coverage](https://github.com/mlops_experiment/blob/main/.github/badges/coverage-ui.svg)](https://mlops_experiment.github.io/coverage-reports/ui/)
[![CI/CD](https://github.com/mlops_experiment/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/mlops_experiment/actions/workflows/ci-cd.yml)
[![Tests](https://github.com/mlops_experiment/actions/workflows/tests.yml/badge.svg)](https://github.com/mlops_experiment/actions/workflows/tests.yml)
[![Build](https://github.com/mlops_experiment/actions/workflows/build-test.yml/badge.svg)](https://github.com/mlops_experiment/actions/workflows/build-test.yml)

A Docker Compose-based project for experimenting with ML agents and observability.

## Project Structure

```
mlops_experiment/
├── docker-compose.yml           # Main compose file
├── agent/                      # ML agent service
│   ├── Dockerfile             
│   ├── requirements.txt        
│   └── src/                    
│       └── main.py            # Agent implementation
└── monitoring/                 # Monitoring setup
    ├── prometheus/
    │   └── prometheus.yml
    └── grafana/
        └── dashboards/
```

## Services

- **Agent**: FastAPI-based ML agent service (port 8000)
- **Prometheus**: Metrics collection (port 9090)
- **Grafana**: Visualization dashboard (port 3000)

## Getting Started

1. Clone the repository
2. Start the services:
   ```bash
   docker-compose up --build
   ```
3. Access the services:
   - Agent: http://localhost:8000
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3000

## Development

The agent service is mounted as a volume, so changes to the Python code will be reflected immediately without rebuilding the container.

## Testing and Coverage

The project uses a comprehensive testing strategy:

- **Unit Tests**: Tests for individual components
- **Integration Tests**: Tests for service interactions
- **Code Coverage**: Minimum 80% coverage requirement
- **CI/CD Pipeline**: Automated testing and coverage reporting

### Running Tests Locally

```bash
# Run agent tests
cd agent
pytest src/test_main.py -v --cov=src --cov-report=term-missing

# Run UI tests
cd ui
pytest src/test_ui.py -v --cov=src --cov-report=term-missing
```

### Coverage Reports

- Coverage reports are automatically generated for each PR and commit to main
- Coverage badges are updated automatically
- Full HTML coverage reports are available on GitHub Pages:
  - [Agent Coverage Report](https://mlops_experiment.github.io/coverage-reports/agent/)
  - [UI Coverage Report](https://mlops_experiment.github.io/coverage-reports/ui/)

## GitHub Workflows

The project uses several GitHub Actions workflows for continuous integration and testing:

### CI/CD Pipeline (ci-cd.yml)
- **Triggers**: On push to main/feature branches and pull requests to main
- **Functions**: Runs tests, builds containers, checks code quality, and deploys (main branch only)
- **Usage**: Comprehensive pipeline for full validation and deployment

### Tests Workflow (tests.yml)
- **Triggers**: On code changes to agent or UI, can be run manually
- **Functions**: Runs tests and generates coverage reports without container builds
- **Usage**: Fast feedback on code changes during development

### Build Test (build-test.yml)
- **Triggers**: On push/PR to main branch, can be run manually
- **Functions**: Validates Docker builds without running tests
- **Usage**: Verify Docker build process works correctly

To manually trigger a workflow:
1. Go to the Actions tab in GitHub
2. Select the workflow you want to run
3. Click "Run workflow" button
4. Select the branch and click "Run workflow"

## Monitoring

- Prometheus metrics are available at `/metrics` endpoint
- Basic request count and latency metrics are implemented
- Grafana can be configured to visualize these metrics

## TODO

### Badge Improvements
- [ ] Add Python version badge
- [ ] Add license badge
- [ ] Improve badge layout with shields.io customizations
- [ ] Add color-coded coverage thresholds

### Testing Documentation
- [ ] Add detailed test case examples
- [ ] Document test fixtures and setup
- [ ] Add integration test scenarios
- [ ] Create testing best practices guide
- [ ] Add troubleshooting guide for common test failures

### Code Structure and Organization
- [ ] Implement layered architecture (API/controllers, services, repositories)
- [ ] Separate business logic from API endpoints
- [ ] Create dedicated directories for each layer
- [ ] Split models into appropriate files
- [ ] Implement proper dependency injection

### Error Handling and Validation
- [ ] Add global exception handler middleware
- [ ] Create custom exception types
- [ ] Implement more detailed validation logic
- [ ] Add proper error logging 
- [ ] Add request/response validation decorators

### Database Improvements
- [ ] Optimize N+1 query issues
- [ ] Add configuration for time-window calculations
- [ ] Implement database migrations with Alembic
- [ ] Consider PostgreSQL for production
- [ ] Add connection pooling and timeouts
- [ ] Add index optimization

### Test Coverage Expansion
- [ ] Increase test coverage to 90%+
- [ ] Add tests for habit completion
- [ ] Create performance/load tests
- [ ] Add integration tests for full workflow
- [ ] Implement proper test data fixtures
- [ ] Add mocking examples

### Documentation
- [ ] Add OpenAPI/Swagger documentation
- [ ] Add docstrings to all functions
- [ ] Document models with field descriptions
- [ ] Create developer guide
- [ ] Add architectural diagrams
- [ ] Create user documentation

### Metrics and Monitoring
- [ ] Add business-specific metrics
- [ ] Use constants for metric names
- [ ] Add histogram buckets for latency metrics
- [ ] Implement health check probes for Kubernetes
- [ ] Add alerting rules
- [ ] Create dashboard templates

### Security
- [ ] Implement OAuth2 or JWT authentication
- [ ] Add role-based access control
- [ ] Implement rate limiting
- [ ] Use environment variables for credentials
- [ ] Add security headers
- [ ] Conduct security audit

### DevOps Improvements
- [ ] Create multi-stage Docker builds
- [ ] Add environment-specific configurations
- [ ] Separate test pipeline from build
- [ ] Create Kubernetes deployment manifests
- [ ] Implement CI/CD for multiple environments
- [ ] Add infrastructure as code 