from prometheus_client import Counter

counter_total = Counter("job_runs_total", "Total runs of jobs", ["job"])
counter_status = Counter("job_runs_status", "Status of jobs", ["job", "status"])
