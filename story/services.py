import feedparser

from django.db.models import Q

from source.models import Source
from story.models import Story


def fetch_stories(user):
    """
    fetch stories from rss for all sources of the company of user and create story
    """
    company = user.subscriber.company

    sources = Source.objects.filter(company=company).select_related("company")

    stories = []

    for source in sources:
        try:
            feed = feedparser.parse(source.url)
        except Exception:
            continue

        for entry in feed.entries:
            title = entry.get("title", "")
            link = entry.get("link")
            summary = entry.get("summary", "")

            if not link:
                continue

            stories.append(
                Story(
                    url=link,
                    company=company,
                    source=source,
                    title=title,
                    body_text=summary,
                    created_by=user,
                    updated_by=user,
                )
            )

    if stories:
        Story.objects.bulk_create(stories, ignore_conflicts=True)


def get_stories(user, query=None, source_id=None):
    qd = {}
    if not user.is_staff:
        qd["company_id"] = user.subscriber.company_id

    if query:
        qd["title__icontains"] = query

    if source_id:
        qd["source_id"] = source_id
        

    return (
        Story.objects.filter(**qd)
        .select_related("source", "created_by", "updated_by")
        .prefetch_related("tagged_companies")
    )

    
def create_or_update_story(form, user):
    story = form.save(commit=False)
    story.company = user.subscriber.company
    if story.pk is None:
        story.created_by = user

    story.updated_by = user
    story.save()
    form.save_m2m()

    return story



