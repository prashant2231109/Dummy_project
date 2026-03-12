from django.shortcuts import render

from source.models import Source
from story.models import Story
from pprint import pprint
import feedparser


def add_story(form, user):
    story = form.save(commit=False)
    story.created_by = user
    story.updated_by = user
    story.company = user.subscriber.company
    story.save()
    form.save_m2m()

    return story


def fetch_stories(user):
    company = user.subscriber.company
    sources = Source.objects.select_related("company").filter(company=company)

    Stories = []

    for source in sources:

        feed = feedparser.parse(source.url)

        for entry in feed.entries:
            title = entry.get("title")
            link = entry.get("link")
            summary = entry.get("summary", "")

            Stories.append(
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

    Story.objects.bulk_create(Stories, ignore_conflicts=True)
