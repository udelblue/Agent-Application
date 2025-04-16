from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, set_default_openai_key

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key from environment variables
print("Loading OpenAI API key from environment variables...")
print("Environment variable OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
    exit(1)
openai.api_key = api_key
# set_default_openai_key(str(apikey))  


# Initialize FastAPI app
app = FastAPI(
    title="Agent and LLM API",
    description="This is an API that allows interaction with agents with tools or LLMs.",
    version="1.0.0"
)

# Define request model
class AgentRequest(BaseModel):
    input_text: str

# Define Metadata for the API documentation
# This will be displayed in the Swagger UI
tags_metadata = [
    {
        "name": "agent",
        "description": "Agent API to interact with OpenAI agents. Agents can leverage tools to perform tasks.", 
    }, 
     {
        "name": "LLM",
        "description": "Leverage a LLM from OpenAI.", 
    }
]

# This is a simple agent that uses a function tool 
@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."

# Create an agent with the function tool
# The agent will be able to call the function
agent = Agent(
    name="Hello world",
    instructions="You are a helpful agent.",
    tools=[get_weather],
)

# Define a POST endpoint to call the OpenAI agent
@app.post("/agent" , tags=["agent"])
async def call_openai_agent(request: AgentRequest):
    try:
        # Call OpenAI Agent SDK
        response = await Runner.run(agent, input=request.input_text)
        return {"response": response.final_output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Define a POST endpoint to call the OpenAI agent
@app.post("/llm" , tags=["LLM"] )
async def call_openai_llm(request: AgentRequest):
    try:
        client = openai.OpenAI(api_key=api_key)
        # Call OpenAI LLM directly
        response = client.chat.completions.create( 
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": request.input_text}],
            max_tokens=150,
            temperature=0.7
        )
        message_content = response.choices[0].message.content.strip() if response.choices[0].message.content else None


        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))