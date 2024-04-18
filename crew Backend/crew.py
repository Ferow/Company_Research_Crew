from job_manager import append_event
from agents import CompanyResearchAgents
from tasks import CompanyResearchTasks
from crewai import Crew

class CompanyResearchCrew:
    def __init__(self, job_id: str):
        self.job_id = job_id
        # Set up the crew that will be used
        self.crew = None
    
    def setup_crew(self, companies: list[str], positions: list[str]):
        print(f"Setting up crew for {self.job_id} with companies {companies} and positions {positions}")
        
        # SETUP AGENTS
        agents = CompanyResearchAgents()
        research_manager = agents.research_manager(companies, positions)
    
        #No need to pass the companies and possitions and the research manager should tell company research
        #manager what to look up
        company_research_agent = agents.company_research_agent()
    
        # Set up the tasks
        tasks = CompanyResearchTasks(self.job_id)
        company_research_tasks = [
            tasks.company_research(company_research_agent, company, positions) for company in companies
        ]
    
        manager_research = tasks.manage_research(research_manager, companies, positions, company_research_tasks)
        
        #Set up the crew
        #* think of it flattening the list / array from company_research_tasks and then put it back into a list
        self.crew = Crew(
            agents = [research_manager, company_research_agent],
            tasks = [*company_research_tasks, manager_research],
            verbose = 2
        )
        
    def kickoff(self):
        # TODO: kickoff the crew
        if not self.crew:
            print(f"No crew found for {self.job_id}")
            return
        
        append_event(self.job_id, "CREW STARTED")
        
        try:
            print(f"Running crew for {self.job_id}")
            results = self.crew.kickoff()
         #  append_event(self.job_id, "CREW COMPLETED")
         #  print(f"Here are the results {results} for job id {self.job_id}")
            return results
        
        except Exception as e:
            append_event(self.job_id, F"CREW FAILED.  Error - {e} ")
            return str(e)