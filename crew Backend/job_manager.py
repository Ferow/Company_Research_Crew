from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime
from threading import Lock

@dataclass
class Event:
    timestamp: datetime
    data: str

@dataclass
class Job:
    status: str
    events: List[Event]
    result: str

jobs_lock = Lock()
jobs:  Dict[str, "Job"] = {}

def append_event(job_id:str, event_data: str):
    #lock the database so we can only update the database one record at a time
    with jobs_lock:
        if job_id not in jobs:
            print(f"Start job: {job_id}")
            jobs[job_id] = Job(
                status="STARTED",
                events=[],
                result=""
            )
        else:
            print("Appending events data to log")
        
        jobs[job_id].events.append(
                Event(
                    timestamp=datetime.now(),
                    data=event_data
                    )
            )