from dotenv import load_dotenv # Import the function
import os

# --- ADD THIS LINE ---
#load_dotenv() 
# This command finds the .env file and loads all the variables into os.environ

from crewai import Agent, Task, Crew, Process
from crewai_tools import VisionTool
#from dotenv import load_dotenv # Recommended for managing API keys
#import os

# Load environment variables from a .env file (optional but highly recommended)
# You would create a .env file in the same directory with:
os.environ['OPENAI_API_KEY']="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"
#OPENAI_API_KEY="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"
print("Attempting to load OPENAI_API_KEY...")
print(f"Key successfully loaded: {bool(os.getenv('OPENAI_API_KEY'))}") 
# After running, this should print "Key successfully loaded: True"

# --- 1. CONFIGURATION ---

# The script will look for this file in the current working directory
IMAGE_FILE_PATH = "Test_SpeedLimit40.jpg" 

# Initialize the VisionTool
# This tool uses the model specified by the environment (e.g., GPT-4-Vision)
vision_tool = VisionTool()

# Agent Configuration (Define the agent's identity)
agents_config = {
    "researcher": {
        "role": "Image Text Extractor and Technical Analyst",
        "goal": "Accurately read and interpret text from uploaded technical images and summarize key data points.",
        "backstory": "An expert in Computer Vision and OCR, specialized in extracting and summarizing technical data from visual inputs, particularly JIRA tickets."
    }
}

# --- 2. AGENT DEFINITION ---

def create_researcher(config: dict) -> Agent:
    '''Creates the Researcher Agent with the VisionTool.'''
    return Agent(
        # The 'llm' argument can be explicitly set here if needed, 
        # otherwise it defaults to the model defined by the environment variable (e.g., gpt-4-turbo)
        config=config["researcher"],
        allow_delegation=False,
        tools=[vision_tool] 
    )

researcher_agent = create_researcher(agents_config)


# --- 3. TASK DEFINITION ---

image_analysis_task = Task(
    description=f"""
    Analyze the attached image file: {IMAGE_FILE_PATH}.
    Your goal is to perform Optical Character Recognition (OCR) to extract all text from the image.
    
    After extraction, analyze the text and generate a structured summary that includes:
    1. The JIRA ticket IDs (e.g., #4748).
    2. The title or main problem described for each ticket (e.g., 'Stop Line False Positive').
    3. The component or system mentioned ('Stop Line/Sign Detection' or 'Automotive Perception').
    
    The final output must be a concise, structured summary.
    """,
    agent=researcher_agent,
    tools=[vision_tool], 
    expected_output="A structured summary of the text extracted from the image, listing the ticket IDs, their titles, and the affected technical system."
)


# --- 4. CREW EXECUTION ---

# Create the crew
analysis_crew = Crew(
    agents=[researcher_agent],
    tasks=[image_analysis_task],
    process=Process.sequential,
    verbose=True  # Set to 2 for detailed output and internal reasoning
)

print("Starting the Vision Analysis Crew...")
# Run the crew
result = analysis_crew.kickoff()

print("\n\n################################################################################")
print("## Final Analysis Result")
print("################################################################################")
print(result)