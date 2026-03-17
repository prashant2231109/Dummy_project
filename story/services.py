import feedparser

from django.shortcuts import render

from source.models import Source
from story.models import Story


def add_story(form, user):
    story = form.save(commit=False)
    story.created_by = user
    story.updated_by = user
    story.company = user.subscriber.company
    story.save()
    form.save_m2m()

    return story


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
