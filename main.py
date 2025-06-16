"""Basic setup example demonstrating how to use the multi-agent LangGraph template."""

import os
import uuid
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

# Import the template components
from src.workflows.multi_agent_supervisor_workflow import (
    MultiAgentSupervisorWorkflow,
)
from src.config.settings import Settings


def main():
    """Run a basic example of the multi-agent system."""

    print("Multi-Agent LangGraph Template - Basic Example")
    print("=" * 50)

    # Initialize settings
    settings = Settings()
    print(f"Using model: {settings.model_name}")
    print(f"Temperature: {settings.temperature}")

    # Create the multi-agent system
    print("\nCreating multi-agent workflow...")
    multi_agent_supervisor_workflow = MultiAgentSupervisorWorkflow(settings)
    workflow = multi_agent_supervisor_workflow.create_complete_workflow()

    # Example conversation
    initial_message = HumanMessage(
        content="Hi! I'm Deepak Kushwaha, I'd like to find some music recommendations."
    )

    # Generate a unique thread ID for this conversation session
    thread_id = uuid.uuid4()

    # Configuration for the conversation
    config = {"configurable": {"thread_id": thread_id, "user_id": "demo_user"}}

    print("\nStarting conversation...")
    print(f"User: {initial_message.content}")

    try:
        # Execute the workflow
        result = workflow.invoke({"messages": [initial_message]}, config=config)

        print("\n Assistant Response:")
        if result.get("messages"):
            for msg in result["messages"]:
                if hasattr(msg, "content"):
                    print(f"  {msg.content}")
                    msg.pretty_print()
                else:
                    print(f"  {msg}")

        print(f"\nCustomer ID: {result.get('customer_id', 'Not verified')}")
        print(f"Loaded Memory: {result.get('loaded_memory', 'None')}")

    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure you have set up your environment variables correctly.")


if __name__ == "__main__":
    """Main execution function."""

    print("LangGraph Multi-Agent Template Examples")
    print("=" * 60)

    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY not found in environment variables.")
        print("Please set your OpenAI API key before running examples.")
        print("\nCreate a .env file with:")
        print("OPENAI_API_KEY=your_api_key_here")
        exit(1)

    try:
        # Run examples
        main()

        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("Next steps:")
        print("  1. Modify the agents in src/agents/")
        print("  2. Add new tools in src/tools/")
        print("  3. Customize workflows in src/workflows/")
        print("  4. Update configuration in src/config/")

    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        print("Please check your configuration and try again.")
