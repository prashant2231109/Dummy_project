from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from dal import autocomplete

from clients.models import Company
from source.forms import SourceForm

from source.models import Source
from story.models import Story


class CompanyAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Company.objects.none()

        if self.q:
            queryset = Company.objects.filter(name__icontains=self.q)[:10]

        return queryset


@login_required
def source_list(request):
    sources = Source.objects.select_related("company").prefetch_related(
        "tagged_companies"
    )
    if not request.user.is_staff:
        sources = sources.filter(company=request.user.subscriber.company)

    paginator = Paginator(sources, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "source/source_list.html",
        {"page_obj": page_obj},
    )


@login_required
def source_search(request):
    query = request.GET.get("q", "")
    sources = Source.objects.select_related("company").prefetch_related(
        "tagged_companies"
    )
    if not request.user.is_staff:
        sources = sources.filter(
            company=request.user.subscriber.company, name__icontains=query
        )
    sources = sources.filter(name__icontains=query)
    paginator = Paginator(sources, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "source/source_list.html",
        {"page_obj": page_obj, "query": query},
    )


@login_required
def source_detail(request, source_id):
    source = get_object_or_404(Source, id=source_id)

    stories = (
        Story.objects.select_related("source")
        .prefetch_related("tagged_companies")
        .filter(source_id=source.id)
    )
    if not request.user.is_staff:
        stories = stories.filter(created_by=request.user)
    return render(request, "source/source_detail.html", {"stories": stories})


@login_required
def source_form(request, source_id=None):
    if source_id:
        source = get_object_or_404(Source, id=source_id)

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

    return render(request, "source/source_form.html", {"form": form})


@login_required
def source_delete(request, source_id):
    source = get_object_or_404(Source, id=source_id)

    if request.method == "POST":
        source.delete()
        return redirect("source:list")
    return render(request, "source/source_delete.html", {"source": source})
