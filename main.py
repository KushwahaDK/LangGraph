"""Basic setup example demonstrating how to use the multi-agent LangGraph template."""

import os
import uuid
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.types import Command

# Import the template components
from src.workflows import MultiAgentWorkflow
from src.config.settings import Settings
from src.databases.database import Database

# Load environment variables
load_dotenv(dotenv_path=".env", override=True)


def main():
    """Main function to run the multi-agent system."""

    print("Multi-Agent LangGraph Execution")
    print("=" * 60)

    # Initialize settings
    settings = Settings()
    print(f"Using model: {settings.model_name}")
    print(f"Temperature: {settings.temperature}")

    # Create the multi-agent system
    print("\nCreating multi-agent workflow...")
    multi_agent_workflow = MultiAgentWorkflow(settings)
    workflow = multi_agent_workflow.build_graph()

    # Example conversation
    initial_message = HumanMessage(
        content="""My customer id is 1. I Like the Rolling Stones. Can You recommend me some music.Also, I want to know the details of my invoice with the highest unit price."""
    )

    # Generate a unique thread ID for this conversation session
    thread_id = uuid.uuid4()

    # Configuration for the conversation
    config = {
        "configurable": {
            "thread_id": thread_id,
            "user_id": "Deepak",
            "db": Database(),
        }
    }

    print("\nStarting conversation...")

    # Execute the workflow
    result = workflow.invoke({"messages": [initial_message]}, config=config)

    user_input = "My phone number is +55 (12) 3923-5555."
    result = workflow.invoke(Command(resume=user_input), config=config)

    # Print the conversation messages to see the verification and subsequent processing.
    for message in result["messages"]:
        message.pretty_print()

    print(f"\nCustomer ID: {result.get('customer_id', 'Not verified')}")
    print(f"Loaded Memory: {result.get('loaded_memory', 'None')}")


if __name__ == "__main__":
    """Main execution function."""

    print("LangGraph Multi-Agent Example")
    print("=" * 60)

    # Check if API key is set
    if not os.getenv("AZURE_OPENAI_API_KEY"):
        print("AZURE_OPENAI_API_KEY not found in environment variables.")
        print("Please set your OpenAI API key before running examples.")
        print("\nCreate a .env file with:")
        print("AZURE_OPENAI_API_KEY=your_api_key_here")
        exit(1)

    # Run examples
    main()
