from crewai import Agent
#from langchain_openai import ChatOpenAI
import os
#from crewai_tools import SerperDevTool
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from tools.internet_search_tools import InternetSearchTool
from tools.youtube_search_tools import YouTubeVideoSearchTool

load_dotenv()

class CompanyResearchAgents():
    def __init__(self):
        # TODO Add Tools
        print("Setting up agents for company research")
        #initalize LLM
        load_dotenv()
        llmurl = os.environ['OPEN_AI_URL']
        llm_api_key = os.environ['OPENAI_API_KEY']
        llm_model_name = os.environ['OPENAI_MODEL_NAME']
        # Create an instance of the OpenAIWrapper
     
        
        self.ollama_llm = Ollama(model="mistral:latest")
        self.searchInternetTool = InternetSearchTool()
        self.youtubeSearchTool = YouTubeVideoSearchTool()
        # TODO: Replace search tool
        #self.searchInternetTool = SerperDevTool()
        
    def research_manager(self, companies: list[str], positions: list[str]) -> Agent:
        return Agent(
            role="Company Research Manager", 
            goal=f"""Generate a list of JSON objects containing the urls for 3 recent blog articles and
                 the url and title for 3 recent YouTube interview, for each position in each company.
                 
                 Companies: {companies}
                 Positions: {positions}
                 
                Important:
                - The final results MUST be a list of JSON objects must include all companies and positions. Do not leave any out.
                - If you can't find information for a specific position, fill in the information with the word "MISSING".
                - Do not generate fake information. Only return the information you find. Nothing else!
                - Do not stop researching until you find the requested information for each position in each company.
                - All the companies and positions exist so keep researching until you find the information for each one.
                - Make sure you each researched position for each company contains 3 blog articles and 3 YouTube interviews.
                """,
            backstory="""As a Company Research Manager, you are responsible for aggregating all the researched information into a list.""",
            verbose=True,
            llm=self.ollama_llm,
            tools=[InternetSearchTool.searchInternet, self.youtubeSearchTool],
            allow_delegation=True
        )
        
    def company_research_agent(self) -> Agent:
        return Agent(
            role="Company Research Agent",
            goal="""Look up the specific positions for a given company and find urls for 3 recent blog articles and
            the url and title for 3 recent YouTube interviews for each person in the specified positions.  It is your job to return this 
            collected information in a JSON object""",
            backstory="""As a company Research Agent, you are responsible for looking up a specific positions
                within a company and gathering relevant information.
                
                Important:
                - Once you've found the information, immediately stop searching for additional information.
                - Only return the requested information.  NOTHING ELSE!
                - Make sure you find the persona name who holds the position.
                - Do not generate fake information.  Only return the information you find.  Nothing else!
                """,
                tools=[InternetSearchTool.searchInternet, self.youtubeSearchTool],
                llm=self.ollama_llm,
                verbose=True
        )
        