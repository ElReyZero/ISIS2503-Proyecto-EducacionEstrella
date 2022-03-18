from ..models import JobListing

def get_job_listings():
    jbs = JobListing.objects.all()
    return jbs

def get_job_listing_by_major(major):
    jbs = JobListing.objects.filter(carrera=major)
    return jbs