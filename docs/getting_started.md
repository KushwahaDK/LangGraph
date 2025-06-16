# Getting Started with Multi-Agent LangGraph Template

This guide will help you get up and running with the Multi-Agent LangGraph Template quickly.

## Prerequisites

- Python 3.9 or higher
- Basic understanding of LangChain and LangGraph concepts
- API keys for OpenAI and LangSmith (optional)

## Quick Setup

### 1. Environment Setup

1. **Copy environment template:**

   ```bash
   cp env_template.txt .env
   ```

2. **Edit `.env` file with your API keys:**

   ```bash
   # Required
   OPENAI_API_KEY=your-openai-api-key-here
   
   # Optional but recommended
   LANGSMITH_API_KEY=your-langsmith-api-key-here
   LANGSMITH_TRACING=true
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### 2. Basic Usage

Run the basic example to verify everything is working:

```bash
python examples/basic_setup.py
```

This will:

- Initialize the database with sample data
- Create music and invoice agents
- Set up the supervisor agent
- Run test queries to verify functionality

## Understanding the Architecture

### Core Components

1. **Agents** (`src/agents/`):
   - `BaseAgent`: Abstract base class for all agents
   - `SupervisorAgent`: Routes queries to appropriate sub-agents
   - `MusicAgent`: Handles music catalog queries
   - `InvoiceAgent`: Handles billing and invoice queries

2. **Tools** (`src/tools/`):
   - Database tools for music and invoice operations
   - Extensible tool system with base tool class

3. **Memory** (`src/memory/`):
   - Short-term memory for conversation context
   - Long-term memory for user preferences
   - Unified memory manager interface

4. **Workflows** (`src/workflows/`):
   - Base workflow patterns
   - Multi-agent workflow orchestration

5. **Configuration** (`src/config/`):
   - Application settings
   - System prompts for different agents

## Customizing for Your Use Case

### Adding a New Agent

1. **Create agent class:**

   ```python
   # src/agents/sub_agents/your_agent.py
   from ..base_agent import BaseAgent
   
   class YourAgent(BaseAgent):
       def __init__(self, llm, tools=None):
           super().__init__(
               name="your_agent",
               description="Handles your specific domain",
               llm=llm,
               tools=tools or []
           )
       
       def process(self, state, config):
           # Your agent logic here
           pass
   ```

2. **Register with supervisor:**

   ```python
   from agents.sub_agents.your_agent import YourAgent
   
   your_agent = YourAgent(llm=llm)
   supervisor.add_sub_agent(your_agent)
   ```

### Adding New Tools

1. **Create tool functions:**

   ```python
   # src/tools/your_tools.py
   from .base_tool import tool
   
   @tool
   def your_custom_tool(param: str) -> str:
       """Description of what your tool does."""
       # Tool implementation
       return result
   ```

2. **Add to agent:**

   ```python
   agent.add_tool(your_custom_tool)
   ```

### Customizing Memory

1. **Extend memory backends:**

   ```python
   # src/memory/your_memory.py
   from .long_term import LongTermMemory
   
   class YourMemoryBackend(LongTermMemory):
       def __init__(self):
           # Your custom memory implementation
           pass
   ```

2. **Configure in settings:**

   ```python
   # src/config/settings.py
   memory_store_type = "your_backend"
   ```

## Advanced Features

### Human-in-the-Loop

The template supports human intervention points for:

- Customer verification
- Manual decision making
- Quality control

### Multi-Modal Support

Extend the template to support:

- Image processing agents
- Document analysis agents
- Voice interaction agents

### Production Deployment

See deployment documentation for:

- Docker containerization
- API endpoint creation
- Monitoring and logging
- Scaling strategies

## Troubleshooting

### Common Issues

1. **Import Errors:**
   - Ensure all dependencies are installed
   - Check Python path configuration

2. **API Key Issues:**
   - Verify `.env` file is properly configured
   - Check API key validity

3. **Database Errors:**
   - Ensure database setup completed successfully
   - Check database permissions

### Getting Help

- Check the documentation in `docs/`
- Review example implementations in `examples/`
- Refer to the original notebook for implementation details

## Next Steps

1. **Customize the agents** for your specific domain
2. **Add new tools** for your use case
3. **Implement proper workflows** with LangGraph
4. **Add testing** for your components
5. **Deploy to production** following best practices

For more detailed information, see the other documentation files in the `docs/` directory.
