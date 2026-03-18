from dal import autocomplete

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, redirect


from story.forms import StoryForm
from story.models import Story
from source.models import Source
from story.services import create_or_update_story, get_stories, get_story_by_id


@login_required
def fetch_stories(request):
    page_number = request.GET.get("page", 1)
    query = request.GET.get("q", "")
    story_id = request.GET.get("story_id")

    stories = get_stories(request.user, query=None)
    story = get_story_by_id(story_id)

    paginator = Paginator(stories, 25)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "story/story_list.html",
        {"page_obj": page_obj, "query": query, "story": story},
    )


@login_required
def create_or_update(request, story_id=None):
    """
    story creation and updation
    """
    if story_id:
        story = Story.objects.get(id=story_id)

        if not request.user.is_staff and story.created_by != request.user:
            messages.error(
                request, "You are not allowed to edit or create this story."
            )
            return redirect("story:list")
    else:
        story = None

    if request.method == "POST":
        form = StoryForm(request.POST, instance=story, request=request)

        if form.is_valid():
            create_or_update_story(form, request.user)

            return redirect("story:list")

    else:
        form = StoryForm(instance=story, request=request)

    return render(request, "story/story_add.html", {"form": form})


@login_required
def delete_story(request, story_id):
    """
    story delete by staff user and created_by user

    """
    story = Story.objects.get(id=story_id)

    if not request.user.is_staff and story.created_by != request.user:
        messages.error(request, "You are not allowed to delete this story.")
        return redirect("story:list")

    if request.method == "POST":
        delete_story(story)
        return redirect("story:list")

    return render(request, "story/story_delete.html", {"story": story})


class SourceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        queryset = Source.objects.only("id", "name")
        if self.q:
            queryset = queryset.filter(name__istartswith=self.q)

        return queryset[:10]
