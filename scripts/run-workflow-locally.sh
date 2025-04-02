#!/bin/bash
# Script to run GitHub workflows locally using act
# Requirements: Docker, act (https://github.com/nektos/act)

# Check if act is installed
if ! command -v act &> /dev/null; then
    echo "Error: 'act' is not installed. Please install it first:"
    echo "  macOS: brew install act"
    echo "  Other: https://github.com/nektos/act#installation"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "Error: Docker is not running. Please start Docker."
    exit 1
fi

# Create a directory for workflow artifacts
mkdir -p .act-artifacts

# Help message
show_help() {
    echo "Usage: $0 [options] [workflow_file]"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -l, --list     List available workflows"
    echo "  -j, --job JOB  Run specific job in the workflow"
    echo "  -e, --event    Specify event type (push, pull_request)"
    echo ""
    echo "Examples:"
    echo "  $0 --list                   # List all workflows"
    echo "  $0 .github/workflows/tests.yml     # Run tests workflow"
    echo "  $0 -j test .github/workflows/tests.yml  # Run only the test job"
    echo "  $0 -e pull_request .github/workflows/ci-cd.yml  # Run as pull request event"
    exit 0
}

# Parse arguments
WORKFLOW=""
JOB=""
EVENT="push"

while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            show_help
            ;;
        -l|--list)
            echo "Available workflows:"
            find .github/workflows -name "*.yml" -o -name "*.yaml" | sort
            exit 0
            ;;
        -j|--job)
            JOB="$2"
            shift
            ;;
        -e|--event)
            EVENT="$2"
            shift
            ;;
        *)
            WORKFLOW="$1"
            ;;
    esac
    shift
done

# Check if workflow file is provided
if [ -z "$WORKFLOW" ]; then
    echo "Error: No workflow file specified."
    show_help
fi

# Check if workflow file exists
if [ ! -f "$WORKFLOW" ]; then
    echo "Error: Workflow file '$WORKFLOW' not found."
    echo "Available workflows:"
    find .github/workflows -name "*.yml" -o -name "*.yaml" | sort
    exit 1
fi

# Build the command
CMD="act -W $WORKFLOW -e .github/workflows/events/$EVENT.json"

if [ ! -z "$JOB" ]; then
    CMD="$CMD -j $JOB"
fi

# Create event directory if it doesn't exist
mkdir -p .github/workflows/events

# Create event payload file if it doesn't exist
if [ ! -f ".github/workflows/events/$EVENT.json" ]; then
    echo "Creating sample $EVENT event payload..."
    mkdir -p .github/workflows/events
    
    if [ "$EVENT" == "push" ]; then
        echo '{
  "ref": "refs/heads/main",
  "repository": {
    "name": "mlops_experiment",
    "owner": {
      "name": "user"
    }
  }
}' > .github/workflows/events/push.json
    elif [ "$EVENT" == "pull_request" ]; then
        echo '{
  "pull_request": {
    "head": {
      "ref": "feature-branch"
    },
    "base": {
      "ref": "main"
    }
  },
  "repository": {
    "name": "mlops_experiment",
    "owner": {
      "name": "user"
    }
  }
}' > .github/workflows/events/pull_request.json
    fi
fi

# Run the workflow
echo "Running workflow: $WORKFLOW"
echo "Event: $EVENT"
if [ ! -z "$JOB" ]; then
    echo "Job: $JOB"
fi
echo "Command: $CMD"
echo "----------------------------------------"

eval "$CMD" 