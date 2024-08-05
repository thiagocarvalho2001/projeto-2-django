from staff_site.models import SiteSetup

def context_processor_example(request):
    return {
    }

def site_setup(request):
    setup = SiteSetup.objects.order_by('-id').first()

    return {
        'site_setup': {
            'title': setup.title,
            'favicon': setup.favicon,
        }
    }