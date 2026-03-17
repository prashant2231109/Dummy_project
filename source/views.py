from urllib import request

from dal import autocomplete

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from company.models import Company
from source.forms import SourceForm
from source.models import Source
from story.models import Story


@login_required
def fetch_sources(request):
    query = request.GET.get("q", "")
    page_number = request.GET.get("page")
    source_id = request.GET.get("source_id")

    sources = Source.objects.select_related(
        "company", "created_by", "updated_by"
    ).prefetch_related("tagged_companies")

    if not request.user.is_staff:
        sources = sources.filter(company=request.user.subscriber.company)

    if query:
        sources = sources.filter(name__icontains=query)

    stories = None
    if source_id:
        stories = Story.objects.filter(source_id=source_id)

    paginator = Paginator(sources, 25)

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "source/source_list.html",
        {
            "page_obj": page_obj,
            "query": query,
            "stories": stories,
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
            source = form.save(commit=False)
            source.updated_by = request.user
            if source.pk is None:
                source.created_by = request.user
            source.company = request.user.subscriber.company
            source.save()
            form.save_m2m()
            return redirect("source:list")

    else:
        form = SourceForm(instance=source, request=request)

    return render(request, "source/source_add.html", {"form": form})


@login_required
def delete(request, source_id):

    source = get_object_or_404(Source, id=source_id)

    if request.method == "POST":
        source.delete()
        return redirect("source:list")
    return render(request, "source/source_delete.html", {"source": source})
