# Dependencies for the main file.
import os
from dotenv import load_dotenv
from pydantic import BaseModel
# from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic
# from langchain_mistralai import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool
import json
import re

# Our environment variables.
load_dotenv()

# Our LLMs
# llm = ChatOpenAI(model = "gpt-3.5-turbo")
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=os.getenv("GEMINI_API_KEY"))
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=os.getenv("GEMINI_API_KEY"))
# Using Google's Gemini API instead of OpenAI or Anthropic due to quota limits

# response = llm.invoke("Hello, how are you?")
# print(response)


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=os.getenv("GEMINI_API_KEY"))
# llm = ChatMistralAI(
#     model="mistral-large-latest", 
#     mistral_api_key =os.getenv("MISTRAL_API_KEY"),
# )
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use neccessary tools. 
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, wiki_tool, save_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = input("What can i help you research? ")
raw_response = agent_executor.invoke({"query": query})

try:
    # Get the raw output string
    output_str = raw_response.get("output")
    
    # Check if the output contains JSON
    json_match = re.search(r'```json\s*(.+?)\s*```', output_str, re.DOTALL)
    
    if json_match:
        # Extract the JSON content from within the code block
        json_str = json_match.group(1).strip()
        
        # Fix common JSON formatting issues
        # Replace trailing commas before closing brackets
        json_str = re.sub(r',\s*(\]|\})', r'\1', json_str)
        
        # Parse the JSON string directly
        result = json.loads(json_str)
        
        # Create a ResearchResponse object
        structured_response = ResearchResponse(
            topic=result.get("topic", "Unknown Topic"),
            summary=result.get("summary", "No summary available"),
            sources=result.get("sources", []),
            tools_used=result.get("tools_used", [])
        )
    else:
        # If no JSON block is found, try direct parsing
        structured_response = parser.parse(output_str)
    
    # Format the output in a more presentable way
    print("\n" + "="*80)
    print(f"\n📝 RESEARCH TOPIC: {structured_response.topic}\n")
    print("📋 SUMMARY:")
    print(f"{structured_response.summary}\n")
    
    if structured_response.sources:
        print("📚 SOURCES:")
        for i, source in enumerate(structured_response.sources, 1):
            print(f"  {i}. {source}")
        print()
    
    if structured_response.tools_used:
        print("🔧 TOOLS USED:")
        for i, tool in enumerate(structured_response.tools_used, 1):
            print(f"  {i}. {tool}")
        print()
    
    print("="*80 + "\n")
    
except Exception as e:
    print("\n❌ Error parsing response:\n")
    print(f"Error details: {e}")
    
    # Try to extract and display the raw output in a readable format
    if isinstance(raw_response, dict) and "output" in raw_response:
        output = raw_response.get("output")
        print("\nRaw output received:")
        print("="*40)
        print(output)
        print("="*40 + "\n")
    else:
        print(f"Raw Response: {raw_response}")
    
    # Print the type and structure of the response to help debug
    print(f"Response type: {type(raw_response)}")
    if isinstance(raw_response, dict):
        print(f"Response keys: {list(raw_response.keys())}")
    print()
    print()