from source.models import Source
from story.models import Story


def get_sources(user, query=None):
    sources = Source.objects.select_related(
        "company", "created_by", "updated_by"
    ).prefetch_related("tagged_companies")

    if not user.is_staff:
        sources = sources.filter(company=user.subscriber.company)

    if query:
        sources = sources.filter(name__icontains=query)

    return sources


def get_stories_by_source(source_id):
    if not source_id: 
        return None
    
    return Story.objects.filter(source_id=source_id)

def get_story(story_id):
    if not story_id:
        return None
    
    return Story.objects.get(id=story_id)

def add_or_update_source(form, user):
    source = form.save(commit=False)
    source.updated_by = user
    if source.pk is None:
        source.created_by = user
    source.company = user.subscriber.company
    source.save()
    form.save_m2m()

    return source


def source_delete(source):
    source.delete()





