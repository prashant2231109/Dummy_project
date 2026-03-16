from urllib import request

from dal import autocomplete
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect

from clients.models import Company
from story.services import add_story, fetch_stories
from story.forms import StoryForm
from story.models import Story


class CompanyAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Company.objects.none()

        if self.q:
            queryset = Company.objects.filter(name__icontains=self.q)[:10]

        return queryset


@login_required
def story_list(request):
    fetch_stories(request.user)

    page_number = request.GET.get("page", 1)

    if request.user.is_staff:
        cache_key = f"stories_staff_page_{page_number}"
    else:
        company_id = request.user.subscriber.company.id
        cache_key = f"stories_company_{company_id}_page_{page_number}"

    page_obj = cache.get(cache_key)

    if not page_obj:
        stories = Story.objects.select_related("source").prefetch_related(
            "tagged_companies"
        )

        if not request.user.is_staff:
            stories = stories.filter(company=request.user.subscriber.company)

        paginator = Paginator(stories, 25)
        page_obj = paginator.get_page(page_number)

        cache.set(cache_key, page_obj, 60 * 5)

    return render(request, "story/story_list.html", {"page_obj": page_obj})


@login_required
def story_search(request):
    query = request.GET.get("q", "")
    stories = Story.objects.select_related("source").prefetch_related(
        "tagged_companies"
    )
    if not request.user.is_staff:
        stories = stories.filter(
            Q(title__icontains=query)
            | Q(body_text__icontains=query)
            | Q(source__name__icontains=query),
            company=request.user.subscriber.company,
        )

    else:
        stories = stories.filter(
            Q(title__icontains=query)
            | Q(body_text__icontains=query)
            | Q(source__name__icontains=query),
        )
    paginator = Paginator(stories, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "story/story_list.html",
        {"page_obj": page_obj, "query": query},
    )


@login_required
def story_detail(request, story_id):
    story = get_object_or_404(
        Story,
        id=story_id,
    )

    return render(request, "story/story_detail.html", {"story": story})


@login_required
def story_form(request, story_id=None):
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

    return render(request, "story/story_form.html", {"form": form})


@login_required
def story_delete(request, story_id):
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
