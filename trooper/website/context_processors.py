from trooper.website.models import Configuration


def website(request):
    return {"website": Configuration.current()}
