from ..models import JobListing

def get_job_listings():
    jbs = JobListing.objects.all()
    return jbs