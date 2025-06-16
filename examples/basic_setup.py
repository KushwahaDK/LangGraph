"""Basic setup example demonstrating how to use the multi-agent LangGraph template."""

import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

# Load environment variables
load_dotenv()

# Import the template components
from src.workflows.multi_agent_supervisor_workflow import create_multi_agent_system
from src.workflows.simple_workflow import create_simple_workflow
from src.config.settings import Settings


def run_basic_example():
    """Run a basic example of the multi-agent system."""

    print("🤖 Multi-Agent LangGraph Template - Basic Example")
    print("=" * 50)

    # Initialize settings
    settings = Settings()
    print(f"Using model: {settings.model_name}")
    print(f"Temperature: {settings.temperature}")

    # Create the multi-agent system
    print("\n📋 Creating multi-agent workflow...")
    workflow = create_multi_agent_system(settings)

    # Example conversation
    initial_message = HumanMessage(
        content="Hi! I'm John Smith, I'd like to find some music recommendations."
    )

    # Configuration for the conversation
    config = {
        "configurable": {"thread_id": "demo_conversation_001", "user_id": "demo_user"}
    }

    print("\n💬 Starting conversation...")
    print(f"User: {initial_message.content}")

    try:
        # Execute the workflow
        result = workflow.invoke({"messages": [initial_message]}, config=config)

        print("\n🤖 Assistant Response:")
        if result.get("messages"):
            for msg in result["messages"]:
                if hasattr(msg, "content"):
                    print(f"  {msg.content}")
                else:
                    print(f"  {msg}")

        print(f"\n✅ Customer ID: {result.get('customer_id', 'Not verified')}")
        print(f"📝 Loaded Memory: {result.get('loaded_memory', 'None')}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure you have set up your environment variables correctly.")


def run_simple_workflow_example():
    """Run a simple workflow example without full complexity."""

    print("\n" + "=" * 50)
    print("🔄 Simple Workflow Example")
    print("=" * 50)

    from langchain_openai import ChatOpenAI

    # Initialize LLM
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1)

    # Create simple workflow
    simple_workflow = create_simple_workflow(llm)

    # Test message
    test_message = HumanMessage(content="What are some popular rock albums?")

    config = {"configurable": {"thread_id": "simple_demo_001"}}

    print(f"\nUser: {test_message.content}")

    try:
        result = simple_workflow.invoke({"messages": [test_message]}, config=config)

        print("\n🤖 Response:")
        if result.get("messages"):
            for msg in result["messages"]:
                if hasattr(msg, "content"):
                    print(f"  {msg.content}")

    except Exception as e:
        print(f"\n❌ Error: {e}")


def demonstrate_workflow_visualization():
    """Demonstrate workflow graph visualization."""

    print("\n" + "=" * 50)
    print("📊 Workflow Visualization")
    print("=" * 50)

    try:
        # Create workflow
        settings = Settings()
        workflow = create_multi_agent_system(settings)

        print("\n🔍 Generating workflow visualization...")

        # Get the graph visualization
        graph_image = workflow.visualize()

        if graph_image:
            print("✅ Workflow graph generated successfully!")
            print("   The graph shows the complete flow:")
            print(
                "   START → verify_info → load_memory → supervisor → create_memory → END"
            )
            print("   (with human-in-the-loop capabilities)")
        else:
            print("⚠️  Graph visualization requires additional dependencies.")
            print("   Install with: pip install pygraphviz")

    except Exception as e:
        print(f"❌ Visualization error: {e}")


def show_configuration_options():
    """Show different configuration options available."""

    print("\n" + "=" * 50)
    print("⚙️  Configuration Options")
    print("=" * 50)

    # Show environment variables
    print("\n📋 Required Environment Variables:")
    print("  OPENAI_API_KEY - Your OpenAI API key")
    print("  TAVILY_API_KEY - Your Tavily API key (optional)")

    print("\n🔧 Settings Configuration:")
    settings = Settings()
    print(f"  Model: {settings.model_name}")
    print(f"  Temperature: {settings.temperature}")
    print(f"  Max Tokens: {settings.max_tokens}")
    print(f"  Memory Store: {settings.memory_store_type}")

    print("\n💾 Memory Options:")
    print("  - 'memory' (default): In-memory storage")
    print("  - 'sqlite': SQLite database storage")
    print("  - Custom: Implement your own memory backend")

    print("\n🤖 Available Sub-agents:")
    print("  - MusicAgent: Handles music catalog queries")
    print("  - InvoiceAgent: Handles invoice and billing queries")
    print("  - Custom: Create your own specialized agents")


if __name__ == "__main__":
    """Main execution function."""

    print("🚀 LangGraph Multi-Agent Template Examples")
    print("=" * 60)

    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found in environment variables.")
        print("Please set your OpenAI API key before running examples.")
        print("\nCreate a .env file with:")
        print("OPENAI_API_KEY=your_api_key_here")
        exit(1)

    try:
        # Run examples
        run_basic_example()
        run_simple_workflow_example()
        demonstrate_workflow_visualization()
        show_configuration_options()

        print("\n" + "=" * 60)
        print("✅ All examples completed successfully!")
        print("💡 Next steps:")
        print("  1. Modify the agents in src/agents/")
        print("  2. Add new tools in src/tools/")
        print("  3. Customize workflows in src/workflows/")
        print("  4. Update configuration in src/config/")

    except KeyboardInterrupt:
        print("\n\n👋 Examples interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        print("Please check your configuration and try again.")
