from datetime import datetime
import json
from uuid import uuid4
from threading import Thread
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from crew import CompanyResearchCrew
from job_manager import append_event, jobs_lock, jobs, Event


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

def kickoff_crew(job_id:str, companies: list[str], positions: list[str]):
    print(f"Running the crew for {job_id} with companies {companies} and positions {positions}")
    results = None
    
    #Setup the crew
    try:
        company_research_crew = CompanyResearchCrew(job_id)
        company_research_crew.setup_crew(companies, positions)
        results = company_research_crew.kickoff()
        print(f"{job_id} is complete. The results of the job are the following {results}")
    except Exception as e:
        print(f"There was an exception running the crew.  Error is {str(e)}")
        append_event(job_id, f"CREW FAILED: {str(e)}")
        with jobs_lock:
            jobs[job_id].status = "ERROR"
            jobs[job_id].result = str(e)
    with jobs_lock:
        jobs[job_id].status = "COMPLETE"
        #print(f"CREW COMPLETED The results of the job are the following {results}")
        jobs[job_id].result = results
        jobs[job_id].events.append(Event(
            data="CREW COMPLETED", timestamp = datetime.now()
        ))

@app.route('/api/crew', methods=['POST'])
def run_crew():
    data = request.json
    if not data or 'companies' not in data or 'positions' not in data:
        abort(400, description="Invalid input data provided.")
        
    job_id = str(uuid4())
    companies = data['companies']
    positions = data['positions']
    
    #run the crew
    thread = Thread(target=kickoff_crew, args=(job_id, companies, positions))
    thread.start()
    return jsonify({'job_id': job_id}), 200

@app.route('/api/crew/<job_id>', methods=['GET'])
def get_status(job_id):
    with jobs_lock:
        #Check to see if jobs exist
        job = jobs.get(job_id)
        if not job:
            abort(404, description="Job not found")
        
        #Parse the JSON Data
        try:
            result_json = json.loads(job.result)
        except Exception as e:
            #print(f"Error in loading job result.  Result is {job.result} and error is {e}")
            result_json = job.result
        

    return jsonify({
        'job_id': job_id,
        'status': job.status,
        'result': result_json,
        'events': [{"timestamp": event.timestamp.isoformat(), "data": event.data} for event in job.events]
    }), 200
    
if __name__ == '__main__':
    app.run(debug=True, port=5001)
    