from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render


from source.forms import SourceForm
from source.models import Source
from story.models import Story
from source.services import (
    get_sources,
    get_stories_by_source,
    get_story,
    add_or_update_source,
    source_delete,
)


@login_required
def fetch_sources(request):
    query = request.GET.get("q", "")
    page_number = request.GET.get("page",1)
    source_id = request.GET.get("source_id")
    story_id  = request.GET.get("story_id")

    sources = get_sources(request.user, query)
    stories = get_stories_by_source(source_id)
    story   = get_story(story_id)

    paginator = Paginator(sources, 25)

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "source/source_list.html",
        {
            "page_obj": page_obj,
            "query": query,
            "stories": stories,
            "story":story
        },
    )


@login_required
def create_or_update(request, source_id=None):
    """
    for source creation and updation
    """
    if source_id:
        source = Source.objects.filter(id=source_id)

    else:
        source = None
    if request.method == "POST":
        form = SourceForm(request.POST, instance=source, request=request)

        if form.is_valid():
            add_or_update_source(form, request.user)
            return redirect("source:list")

    else:
        form = SourceForm(instance=source, request=request)

    return render(request, "source/source_add.html", {"form": form})


@login_required
def delete_source(request, source_id):

    source = get_object_or_404(Source, id=source_id)

    if request.method == "POST":
        source_delete(source)
    return render(request, "source/source_delete.html", {"source": source})
