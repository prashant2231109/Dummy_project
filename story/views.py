from dal import autocomplete

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.core.cache import cache
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, redirect


from story.forms import StoryForm
from story.models import Story
from source.models import Source
from story.services import create_or_update_story, get_stories


from django.http import JsonResponse


@login_required
@require_GET
def fetch_stories(request):
    page_number = request.GET.get("page", 1)
    query = request.GET.get("q", "")
    source_id = request.GET.get("source_id")

    stories = get_stories(request.user, query, source_id)

    paginator = Paginator(stories, 25)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "story/story_list.html",
        {"page_obj": page_obj, "query": query},
    )

    # data = {
    #     "results": list(page_obj.object_list.values()),
    #     "total_pages": paginator.num_pages,
    #     "current_page": page_obj.number,
    #     "has_next": page_obj.has_next(),
    #     "has_previous": page_obj.has_previous(),
    # }

    # return JsonResponse(data)


@login_required
def create_or_update(request, story_id=None):
    """
    story creation and updation
    """
    if request.method == "POST":
        form = StoryForm(request.POST, request=request)

        if form.is_valid():
            create_or_update_story(form, request.user)
            return redirect("story:list")
    else:
        story = None
        if story_id:
            try:
                qd = {"id": story_id}
                if not request.user.is_staff:
                    qd["created_by"] = request.user
                story = Story.objects.get(**qd)
            except Story.DoesNotExist:
                messages.error(request, "Story not found.")
                return redirect("story:list")
        form = StoryForm(instance=story, request=request)

    return render(request, "story/story_add.html", {"form": form})


@login_required
@require_POST
def delete_story(request, story_id):
    """
    story delete by staff user and created_by user

    """
    qd = {"id": story_id}

    if not request.user.is_staff:
        qd["created_by"] = request.user

    Story.objects.filter(**qd).delete()
    return redirect("story:list")


class SourceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        queryset = Source.objects.only("id", "name")
        if self.q:
            queryset = queryset.filter(name__istartswith=self.q)

        return queryset[:10]
    


def new_stories(request):
    return render(request, "story/index.html", context={})
