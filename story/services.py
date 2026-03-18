import feedparser

from django.db.models import Q
from django.shortcuts import render

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


def get_stories(user, query=None):
    stories = Story.objects.select_related(
        "source",
        "created_by",
        "updated_by",
    ).prefetch_related("tagged_companies")

    if not user.is_staff:
        stories = stories.filter(company=user.subscriber.company)

    if query:
        search_filter = (
            Q(title__icontains=query)
            | Q(body_text__icontains=query)
            | Q(source__name__icontains=query)
        )
        stories = stories.filter(search_filter)

    return stories


def get_story_by_id(story_id):
    if not story_id:
        return None
    return Story.objects.get(id=story_id)


def create_or_update_story(form, user):
    story = form.save(commit=False)
    story.company = user.subscriber.company
    if story.pk is None:
        story.created_by = user

    story.updated_by = user
    story.save()
    form.save_m2m()

    return story


def story_delete(story):
    story.delete()
