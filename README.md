# ML Agent Experiment

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

## Monitoring

- Prometheus metrics are available at `/metrics` endpoint
- Basic request count and latency metrics are implemented
- Grafana can be configured to visualize these metrics 