from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect, render

from clients.forms import SourceForm
from story.models import Story

from .services import create_source
from .models import Source


@login_required
def add_source(request):
    if request.method == "POST":
        form = SourceForm(request.POST, request=request)
        if form.is_valid():
            create_source(form, request.user)
            return redirect("source:list")
    else:
        form = SourceForm(request=request)
    return render(request, "source/source_create.html", {"form": form})


@login_required
def source_list(request):
    sources = Source.objects.filter(company=request.user.subscriber.company)
    return render(
        request, "source/source_list.html", {"sources": sources}
    )


@login_required
def source_detail(request, source_id):
    stories = Story.objects.filter(source_id=source_id)
    print(stories)
    return render(
        request, "source/source_detail.html", {"stories": stories}
    )

@login_required
def source_update(request,source_id):
    source = get_object_or_404(Source, id=source_id)
    if request.method == "POST":
        form=SourceForm(request.POST,instance=source,request=request)

        if form.is_valid():
            source=form.save(commit=False)
            source.updated_by = request.user
            source.company = request.user.subscriber.company
            source.save()
            form.save_m2m()
            return redirect("source:list")
        
    else:
        form=SourceForm(instance=source,request=request)

    return render(request,"source/source_update.html",{"form":form})


def source_delete(request,source_id):
    source = get_object_or_404(Source, id=source_id)
    if request.method == "POST":
        source.delete()
        return redirect("source:list")
    return render(request,"source/source_delete.html",{"source":source})
    




        

