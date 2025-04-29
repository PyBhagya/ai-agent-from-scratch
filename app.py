import os
import streamlit as st
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool

# Load environment variables
load_dotenv()

# Define the research response model
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# Set up the page configuration
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔍",
    layout="wide"
)

# Create a header
st.title("🔍 AI Research Assistant")
st.markdown("Ask me anything, and I'll research it for you using the web and Wikipedia.")

# Initialize session state for chat history and responses
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
# Helper function to convert ResearchResponse to a dictionary
def response_to_dict(response):
    if isinstance(response, ResearchResponse):
        return {
            "topic": response.topic,
            "summary": response.summary,
            "sources": response.sources,
            "tools_used": response.tools_used
        }
    return response

# Function to generate response
def generate_research(query):
    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro", 
        google_api_key=os.getenv("GEMINI_API_KEY")
    )
     # llm = ChatMistralAI(
    #     model="mistral-large-latest", 
    #     mistral_api_key =os.getenv("MISTRAL_API_KEY"),
    # )
    
    # Set up the parser
    parser = PydanticOutputParser(pydantic_object=ResearchResponse)
    
    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are a research assistant that will help generate a research paper.
                Answer the user query and use necessary tools. 
                Wrap the output in this format and provide no other text\n{format_instructions}
                """,
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{query}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    ).partial(format_instructions=parser.get_format_instructions())
    
    # Set up the tools
    tools = [search_tool, wiki_tool, save_tool]
    
    # Create the agent
    agent = create_tool_calling_agent(
        llm=llm,
        prompt=prompt,
        tools=tools
    )
    
    # Create the agent executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    # Get the response
    with st.spinner("Researching... This may take a moment."):
        raw_response = agent_executor.invoke({"query": query})
    
    # Parse the response
    try:
        # Get the raw text from the response
        raw_text = raw_response.get("output")
        
        # Handle different response formats
        if isinstance(raw_text, str):
            text_to_parse = raw_text
        elif isinstance(raw_text, list) and len(raw_text) > 0:
            if isinstance(raw_text[0], dict) and "text" in raw_text[0]:
                text_to_parse = raw_text[0]["text"]
            else:
                text_to_parse = str(raw_text[0])
        else:
            text_to_parse = str(raw_response)
            
        # Clean up the text if it contains JSON markers
        if "```json" in text_to_parse:
            text_to_parse = text_to_parse.split("```json")[1].split("```")[0].strip()
        
        # Parse the response
        structured_response = parser.parse(text_to_parse)
        return structured_response
    except Exception as e:
        st.error(f"Error parsing response: {e}")
        # Return a simplified version for display
        if "output" in raw_response and raw_response["output"]:
            return {"error": str(e), "raw_response": raw_response["output"]}
        return {"error": str(e), "raw_response": raw_response}

# Create a sidebar with information
with st.sidebar:
    st.header("About")
    st.info(
        """
        This AI Research Assistant uses:
        - Google's Gemini AI model
        - Web search via DuckDuckGo
        - Wikipedia for factual information
        
        Ask any research question and get a structured response with sources.
        """
    )
    
    # Add a clear chat button
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# Create the main chat interface
query = st.chat_input("What would you like me to research?")

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant", avatar="🔍"):
            content = message["content"]
            if isinstance(content, dict) and "topic" in content and "summary" in content:
                st.write(f"**Topic:** {content['topic']}")
                st.write(f"**Summary:**\n{content['summary']}")
                
                st.write("**Sources:**")
                for source in content['sources']:
                    st.write(f"- {source}")
                
                st.write("**Tools Used:**")
                for tool in content['tools_used']:
                    st.write(f"- {tool}")
            elif isinstance(content, dict) and "raw_response" in content:
                st.write("I encountered an error while researching, but here's what I found:")
                st.write(content["raw_response"])
            else:
                st.write("I encountered an error while researching. Please try again.")
                st.write(content)

# Process the user query
if query:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": query})
    
    # Display user message
    with st.chat_message("user"):
        st.write(query)
    
    # Generate and display response
    with st.chat_message("assistant", avatar="🔍"):
        response = generate_research(query)
        
        if isinstance(response, ResearchResponse):
            st.write(f"**Topic:** {response.topic}")
            st.write(f"**Summary:**\n{response.summary}")
            
            st.write("**Sources:**")
            for source in response.sources:
                st.write(f"- {source}")
            
            st.write("**Tools Used:**")
            for tool in response.tools_used:
                st.write(f"- {tool}")
            
            # Add response to chat history as a dictionary
            st.session_state.chat_history.append({"role": "assistant", "content": response_to_dict(response)})
        elif isinstance(response, dict) and "error" in response:
            st.error(f"Error: {response['error']}")
            
            # Try to display raw response in a readable format
            if "raw_response" in response:
                raw_output = response["raw_response"]
                
                # Check if the raw output contains JSON
                if isinstance(raw_output, str) and "```json" in raw_output:
                    json_text = raw_output.split("```json")[1].split("```")[0].strip()
                    st.json(json_text)
                elif isinstance(raw_output, str):
                    st.text(raw_output)
                else:
                    st.write("Raw response:")
                    st.write(raw_output)
            
            st.write("I encountered an error while researching. Please try again.")
        else:
            st.write("I encountered an error while researching. Please try again.")
            st.write("Raw response:")
            st.write(response)
