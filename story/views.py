from dal import autocomplete

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect


from story.forms import StoryForm
from story.models import Story
from source.models import Source


# @

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def fetch_stories(request):
    page_number = request.GET.get("page", 1)
    query = request.GET.get("q", "")
    story_id = request.GET.get("story_id")

    stories = Story.objects.select_related(
        "source",
        "created_by",
        "updated_by",
    ).prefetch_related("tagged_companies")

    if not request.user.is_staff:
        stories = stories.filter(company=request.user.subscriber.company)

    if query:
        search_filter = (
            Q(title__icontains=query)
            | Q(body_text__icontains=query)
            | Q(source__name__icontains=query)
        )
        stories = stories.filter(search_filter)

    story = None
    if story_id:
        story = Story.objects.get(id=story_id)

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
        story = get_object_or_404(
            Story,
            id=story_id,
        )

        if not request.user.is_staff and story.created_by != request.user:
            messages.error(request, "You are not allowed to edit this story.")
            return redirect("story:list")
    else:
        story = None

    if request.method == "POST":
        form = StoryForm(request.POST, instance=story, request=request)

        if form.is_valid():
            story = form.save(commit=False)
            story.company = request.user.subscriber.company
            if story.pk is None:
                story.created_by = request.user

            story.updated_by = request.user
            story.save()
            form.save_m2m()
            return redirect("story:list")

    else:
        form = StoryForm(instance=story, request=request)

    return render(request, "story/story_add.html", {"form": form})


@login_required
def delete(request, story_id):
    """
    story delete by staff user and created_by user

    """
    story = get_object_or_404(
        Story,
        id=story_id,
    )
    if not request.user.is_staff and story.created_by != request.user:
        messages.error(request, "You are not allowed to delete this story.")
        return redirect("story:list")

    if request.method == "POST":
        story.delete()
        return redirect("story:list")

    return render(request, "story/story_delete.html", {"story": story})


class SourceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        queryset = Source.objects.only("id", "name")
        if self.q:
            queryset = queryset.filter(name__istartswith=self.q)

        return queryset[:10]
