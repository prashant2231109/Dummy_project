from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST

from clients.forms import StoryForm
from clients.models import Company
from source.models import Source
from story.services import add_story

from .models import Story


@login_required
def story_list(request):
    stories = Story.objects.select_related("source").prefetch_related("tagged_companies").filter(company=request.user.subscriber.company)
    return render(request, "story/story_list.html", {"stories": stories})


def story_create(request):
    if request.method == "POST":
        form = StoryForm(request.POST, request=request)
     
        if form.is_valid():
            add_story(form,request.user)
            return redirect("story:list")
           
        
    else:
        form = StoryForm(request=request)

    return render(request, "story/story_create.html", {"form": form})


def story_detail(request, story_id):
    story = Story.objects.get(id=story_id)

    return render(request, "story/story_detail.html", {"story": story})


def story_update(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    if request.method == "POST":
        form = StoryForm(request.POST, instance=story)
        
        if form.is_valid():
            story = form.save(commit=False)
            story.updated_by = request.user
            story.save()
            form.save_m2m()
            return redirect("story:list")

    else:
        form = StoryForm(instance=story)

    return render(request, "story/story_update.html", {"form": form})


def story_delete(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    if request.method == "POST":
        story.delete()
        return redirect("story:list")

    return render(request, "story/story_delete.html", {"story": story})
