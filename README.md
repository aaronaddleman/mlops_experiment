# ML Agent Experiment

[![Agent Coverage](https://codecov.io/gh/mlops_experiment/branch/main/graph/badge.svg?flag=unittests&path=agent/src)](https://codecov.io/gh/mlops_experiment)
[![UI Coverage](https://codecov.io/gh/mlops_experiment/branch/main/graph/badge.svg?flag=unittests&path=ui/src)](https://codecov.io/gh/mlops_experiment)
[![CI/CD](https://github.com/mlops_experiment/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/mlops_experiment/actions/workflows/ci-cd.yml)

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

- Coverage reports are automatically generated for each pull request
- Coverage changes are commented on PRs
- Historical coverage data is available on Codecov

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