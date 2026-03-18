
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import  redirect, render,get_object_or_404


from source.forms import SourceForm
from source.models import Source
from source.services import get_sources, add_or_update_source



@login_required
def fetch_sources(request):
    query = request.GET.get("q", "")
    page_number = request.GET.get("page", 1)
   
    sources = get_sources(request.user, query)
    page_obj = Paginator(sources, 5).get_page(page_number)

    context = {
        "page_obj": page_obj,
        "query": query
    }

    return render(request, "source/source_list.html", context=context)


@login_required
def create_or_update(request, source_id=None):
    """
    for source creation and updation
    """
    source = None

    try:
        if source_id:
            source = Source.objects.get(id=source_id)

        if request.method == "POST":
            form = SourceForm(request.POST, instance=source, request=request)

            if form.is_valid():
                add_or_update_source(form, request.user)
                return redirect("source:list")

        else:
            form = SourceForm(instance=source, request=request)

    except Exception:
        messages.error(request, "Something went wrong")
        return redirect("source:list")

    return render(request, "source/source_add.html", {"form": form})


@login_required
def delete_source(request, source_id):
 
    source = get_object_or_404(Source, id=source_id)

    if request.method == "POST":
            source.delete()

    return render(request, "source/source_delete.html", {"source": source})
