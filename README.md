# CIRNO Questions Generator Agent

A multi-agent question generation system built with Google's Agent Development Kit (ADK) and A2A (Agent-to-Agent) framework. This agent is part of the CIRNO multi-agent system designed to intelligently generate educational questions based on specified topics.

## Features

- **Multi-agent Architecture**: Orchestrates specialized agents for question planning, generation, validation, and ordering
- **Intelligent Question Generation**: Creates contextually relevant questions with varying difficulty levels
- **External Resource Integration**: Leverages web search and academic resources for comprehensive question creation
- **Validation Pipeline**: Includes investigation and refinement loops to ensure question quality
- **A2A Compliant**: Built on the Agent-to-Agent protocol for interoperability with other AI agents
- **Docker Support**: Containerized deployment with easy configuration
- **Customizable LLM Backend**: Supports various LLM providers through LiteLLM

## System Architecture

The system is composed of several specialized agents working together:

```
┌─────────────────────────────────────────────────────────┐
│                  Router Agent                           │
│  (cirno_questions_generator_agent)                      │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │  Analysis   │  │  Questions      │  │  Remote     │ │
│  │   Agent     │  │  Setter Agent   │  │   Agents    │ │
│  └─────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Core Components

1. **Router Agent** (`cirno_questions_generator_agent/`)
   - Main entry point and orchestrator
   - Routes requests to appropriate sub-agents
   - Manages agent state and communication

2. **Questions Features Analysis Agent** (`questions_features_analysis_agent/`)
   - Analyzes topic characteristics and requirements
   - Determines appropriate question types and difficulty levels
   - Provides structured analysis for question generation

3. **Questions Setter Agent** (`questions_setter_agent/`)
   - Core question generation pipeline
   - Includes planning, generation, validation, and ordering stages
   - Iteratively refines questions through investigation loops

4. **Remote Agents** (`remote_agents/`)
   - **Web Search Agent**: Fetches relevant information from the web
   - **Math & Science Agent**: Provides domain-specific academic resources

## Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/StudentAssistantTeam/CIRNO_QuestionsGeneratorAgent.git
   cd CIRNO_QuestionsGeneratorAgent
   ```

2. **Install dependencies with uv**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   Create the required `.env` files based on the templates:

   ```bash
   # Copy example environment files
   cp cirno_questions_generator_agent.env.example cirno_questions_generator_agent.env
   cp questions_features_analysis_agent.env.example questions_features_analysis_agent.env
   cp questions_setter_agent.env.example questions_setter_agent.env
   cp remote_agents.env.example remote_agents.env
   ```

   Edit each file to configure your LLM provider settings.

### Configuration

#### LLM Configuration
The system uses LiteLLM for model abstraction. Configure your preferred LLM provider:

```env
# cirno_questions_generator_agent.env
LLM_MODEL_NAME=dashscope/qwen-plus  # or your preferred model
LLM_API_KEY=your-api-key-here
LLM_BASE_URL=https://api.provider.com/v1
```

Supported providers include OpenAI, Anthropic, Google, Azure, and any LiteLLM-compatible endpoint.

#### Server Configuration
```env
# cirno_questions_generator_agent.env (additional settings)
A2A_HOST=localhost
A2A_PORT=4004
USE_DB_TASK_STORE=false
USE_DB_PUSH_NOTIFICATIONS=false
```

### Running the Agent

#### Local Development

1. **Start the A2A server**
   ```bash
   uv run questions_generator_agent_app
   ```

   The server will start at `http://localhost:4004/`

2. **Verify the server is running**
   ```bash
   curl http://localhost:4004/
   ```

#### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build --build-arg MIRROR=https://pypi.tuna.tsinghua.edu.cn/simple -t cirno-questions-agent .
   ```

2. **Run the container**
   ```bash
   docker run -p 4004:4004 -v $(pwd)/.env:/app/.env cirno-questions-agent
   ```

## API Usage

### Agent Card
The agent exposes an A2A-compliant API. You can access the agent card at:

```
GET http://localhost:4004/
```

### Generating Questions

Send a POST request to the agent with the following JSON structure:

```json
{
  "topic": "Gravity",
  "has_sample_questions": false,
  "questions_number": 5
}
```

## Project Structure

```
CIRNO_QuestionsGeneratorAgent/
├── cirno_questions_generator_agent/     # Main router agent
│   ├── agent.py                         # Router agent definition
│   ├── agent_executor.py                # Agent executor logic
│   ├── config.py                        # Configuration settings
│   ├── data_model.py                    # Pydantic schemas
│   ├── main.py                          # A2A server entry point
│   ├── prompt.py                        # Agent prompts
│   └── logger_config.py                 # Logging configuration
├── questions_features_analysis_agent/   # Analysis agent
│   ├── agent.py                         # Analysis agent definition
│   ├── config.py                        # Configuration
│   ├── data_model.py                    # Schemas
│   ├── planner.py                       # Custom planner
│   └── prompt.py                        # Prompts
├── questions_setter_agent/              # Question generation agent
│   ├── agent.py                         # Setter agent definition
│   ├── config.py                        # Configuration
│   ├── data_model.py                    # Schemas
│   └── prompt.py                        # Prompts
├── remote_agents/                       # External resource agents
│   ├── web_search_agent.py              # Web search capabilities
│   ├── math_and_science_agent.py        # Academic resources
│   └── config.py                        # Configuration
├── tools/                               # Utility tools
│   └── util_tools.py                    # Shared tool functions
├── utility/                             # Shared utilities
│   └── shared_info.py                   # Shared constants and state keys
├── pyproject.toml                       # Project dependencies
├── uv.lock                              # Locked dependencies
├── Dockerfile                           # Container configuration
├── entrypoint.sh                        # Container entry script
└── *.env                                # Environment configuration files
```

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `LLM_MODEL_NAME` | LiteLLM model identifier | `dashscope/qwen-plus` |
| `LLM_API_KEY` | API key for LLM provider | `sk-...` |
| `LLM_BASE_URL` | Base URL for LLM API | `https://api.provider.com/v1` |

### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `A2A_HOST` | `localhost` | Hostname for A2A server |
| `A2A_PORT` | `4004` | Port for A2A server |
| `USE_DB_TASK_STORE` | `false` | Use database for task storage |
| `USE_DB_PUSH_NOTIFICATIONS` | `false` | Use database for push notifications |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Google's Agent Development Kit (ADK)](https://github.com/google/adk)
- Uses [LiteLLM](https://github.com/BerriAI/litellm) for LLM abstraction

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.