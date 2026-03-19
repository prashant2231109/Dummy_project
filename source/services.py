from source.models import Source
from story.models import Story


def get_sources(user, query=None):
    qd = {}

    if query:
        qd["name__icontains"] = query

    if not user.is_staff:
        qd["company_id"] =  user.subscriber.company_id

    return Source.objects.filter(**qd).select_related(
        "company", "created_by", "updated_by"
    ).prefetch_related("tagged_companies")


def add_or_update_source(form, user):
    source = form.save(commit=False)
    source.updated_by = user
    if source.pk is None:
        source.created_by = user
    source.company = user.subscriber.company
    source.save()
    form.save_m2m()

    return source






