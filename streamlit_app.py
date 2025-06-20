"""
Streamlit Chat Interface for LangGraph Multi-Agent System

This application provides a simple chat interface to interact with the
multi-agent system without conversation history persistence.
"""

import streamlit as st
import uuid
import os
import traceback
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.types import Command

# Import the template components
from src.workflows import MultiAgentWorkflow
from src.config.settings import Settings

# Load environment variables
load_dotenv(dotenv_path=".env", override=True)

# Initialize session state
if "workflow" not in st.session_state:
    st.session_state.workflow = None
if "multi_agent_workflow" not in st.session_state:
    st.session_state.multi_agent_workflow = None
if "system_initialized" not in st.session_state:
    st.session_state.system_initialized = False
if "conversation_data" not in st.session_state:
    st.session_state.conversation_data = None


@st.cache_resource
def initialize_system():
    """Initialize the multi-agent system with caching."""
    try:
        # Initialize settings
        settings = Settings()

        # Create the multi-agent system
        multi_agent_workflow = MultiAgentWorkflow(settings)
        workflow = multi_agent_workflow.build_graph()

        return workflow, multi_agent_workflow, True
    except Exception as e:
        return None, None, False


def process_user_input(workflow, multi_agent_workflow, user_input, user_name="User"):
    """Process user input through the multi-agent workflow."""
    try:
        # Create a human message
        initial_message = HumanMessage(content=user_input)

        # Generate a unique thread ID for this session (no persistence)
        thread_id = uuid.uuid4()

        # Configuration for the conversation
        config = {
            "configurable": {
                "thread_id": thread_id,
                "user_id": user_name,
                "llm": multi_agent_workflow.llm,
                "structured_llm": multi_agent_workflow.structured_llm,
            }
        }

        # Execute the workflow
        result = workflow.invoke({"messages": [initial_message]}, config=config)

        return result, config

    except Exception as e:
        st.error(f"Error processing input: {str(e)}")
        return None, None


def continue_workflow(workflow, verification_input, config):
    """Continue the workflow with verification input."""
    try:
        # Send verification input as a command
        result = workflow.invoke(Command(resume=verification_input), config=config)
        return result
    except Exception as e:
        st.error(f"Error in verification: {str(e)}")
        return None


def display_response(result):
    """Display the agent's response in a user-friendly format."""
    if not result:
        return

    # Extract messages from the result
    messages = result.get("messages", [])

    if not messages:
        st.warning("No response received from the agent.")
        return

    # Display the conversation
    for i, message in enumerate(messages):
        if hasattr(message, "content") and message.content:
            # Skip the initial user message to avoid duplication
            if i == 0 and hasattr(message, "type") and message.type == "human":
                continue

            # Determine message type and display accordingly
            if hasattr(message, "type"):
                if message.type == "human":
                    st.chat_message("user").write(message.content)
                elif message.type == "ai":
                    st.chat_message("assistant").write(message.content)
                elif message.type == "system":
                    st.chat_message("assistant").write(message.content)
                elif message.type == "tool":
                    # Display tool results in an expandable section
                    with st.expander("🔧 Tool Execution Details"):
                        st.code(str(message.content), language="json")
                else:
                    st.chat_message("assistant").write(message.content)
            else:
                st.chat_message("assistant").write(str(message.content))

    # Display additional information if available
    if result.get("customer_id"):
        st.success(f"🆔 Customer verified: {result['customer_id']}")

    if result.get("loaded_memory"):
        with st.expander("🧠 Loaded Memory"):
            st.json(result["loaded_memory"])


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="LangGraph Multi-Agent Chat",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    # Title and header
    st.title("🤖 LangGraph Multi-Agent Chat")
    st.markdown("**Ask about music recommendations or invoice details!**")

    # Check API key
    if not os.getenv("AZURE_OPENAI_API_KEY"):
        st.error("🔑 AZURE_OPENAI_API_KEY not found in environment variables.")
        st.info("Please set your Azure OpenAI API key in your .env file:")
        st.code("AZURE_OPENAI_API_KEY=your_api_key_here")
        return

    # Initialize system
    if not st.session_state.system_initialized:
        with st.spinner("Initializing multi-agent system..."):
            workflow, multi_agent_workflow, success = initialize_system()

            if success:
                st.session_state.workflow = workflow
                st.session_state.multi_agent_workflow = multi_agent_workflow
                st.session_state.system_initialized = True
                st.success("✅ Multi-agent system initialized successfully!")
            else:
                st.error(
                    "Failed to initialize the system. Please check your configuration."
                )
                return

    # Sidebar with information
    with st.sidebar:
        st.header("💡 How to Use")
        st.markdown(
            """
        **This chat interface supports:**
        - 🎵 Music recommendations 
        - 📄 Invoice queries
        - 🔍 Customer information lookup
        
        **Example queries:**
        - "My customer ID is 1. I like The Beatles, recommend some music"
        - "Customer ID 1. Show me my invoice details"
        - "My customer id is 1. What's my highest invoice amount?"
        """
        )

        st.header("⚙️ Configuration")
        if st.session_state.multi_agent_workflow:
            st.text(
                f"Model: {st.session_state.multi_agent_workflow.settings.model_name}"
            )
            st.text(
                f"Temperature: {st.session_state.multi_agent_workflow.settings.temperature}"
            )

        # User name input
        user_name = st.text_input(
            "Your Name (optional)", value="User", placeholder="Enter your name"
        )

        # Clear conversation button
        if st.button("🔄 Clear Conversation"):
            st.session_state.conversation_data = None
            st.rerun()

    # Main chat interface
    st.markdown("---")

    # User input
    user_input = st.text_area(
        "💬 Ask me anything about music or invoices:",
        placeholder="Type your question here... (e.g., 'My customer ID is 1. I like rock music, can you recommend something?' or 'Customer ID 1. Show me my invoice details')",
        height=100,
    )

    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Send Message", use_container_width=True):
            if user_input.strip():
                with st.spinner("🤔 Processing your request..."):
                    # Process the user input
                    result, config = process_user_input(
                        st.session_state.workflow,
                        st.session_state.multi_agent_workflow,
                        user_input,
                        user_name,
                    )

                    if result:
                        # Store conversation data for potential verification
                        st.session_state.conversation_data = {
                            "result": result,
                            "config": config,
                            "user_input": user_input,
                        }

                        # Check if we need verification (customer_id not set)
                        if not result.get("customer_id"):
                            st.info(
                                "📱 Phone number verification may be required. Please provide your phone number if requested."
                            )

                        # Display the result
                        display_response(result)
                    else:
                        st.error("Failed to process your request. Please try again.")
            else:
                st.warning("Please enter a message before sending.")

    # Verification input section
    if st.session_state.conversation_data and not st.session_state.conversation_data[
        "result"
    ].get("customer_id"):
        st.markdown("---")
        st.subheader("📱 Phone Number Verification")
        st.info("If you need to verify your phone number, enter it below:")

        verification_input = st.text_input(
            "Phone Number:", placeholder="+1 (555) 123-4567"
        )

        if st.button("✅ Verify Phone Number"):
            if verification_input.strip():
                with st.spinner("Verifying phone number..."):
                    final_result = continue_workflow(
                        st.session_state.workflow,
                        verification_input,
                        st.session_state.conversation_data["config"],
                    )

                    if final_result:
                        st.success("✅ Verification complete!")
                        display_response(final_result)
                        # Clear conversation data after verification
                        st.session_state.conversation_data = None
                    else:
                        st.error("Verification failed. Please try again.")
            else:
                st.warning("Please enter your phone number for verification.")

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.8em;'>"
        "Powered by LangGraph Multi-Agent System | No conversation history is retained"
        "</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
