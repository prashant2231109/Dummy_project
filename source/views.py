from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST, require_GET


from source.forms import SourceForm
from source.models import Source
from source.services import get_sources, add_or_update_source


@login_required
@require_GET
def fetch_sources(request):
    query = request.GET.get("q", "")
    page_number = request.GET.get("page", 1)

    sources = get_sources(request.user, query)
    page_obj = Paginator(sources, 5).get_page(page_number)

    context = {"page_obj": page_obj, "query": query}
    return render(request, "source/source_list.html", context=context)


@login_required
def create_or_update(request, source_id=None):
    """
    for source creation and updation
    """
  

    if request.method == "POST":
        form = SourceForm(request.POST, request=request)
        if form.is_valid():
            add_or_update_source(form, request.user)
            return redirect("source:list")
        
    

    else:
        source = None
    
        if source_id: 
            try:
                qd = {"id": source_id}
                if not request.user.is_staff:
                    qd["created_by"] = request.user  
                    
                source = Source.objects.filter(**qd)
            except Source.DoesNotExist:
                messages.error(request, "Source not found.")
                return redirect("source:list")

        form = SourceForm(instance=source, request=request)
    return render(request, "source/source_add.html", {"form": form})


@login_required
@require_POST
def delete_source(request, source_id):
    qd = {"id": source_id}

    if not request.user.is_staff:
        qd["created_by"] = request.user

    Source.objects.filter(**qd).delete()
    return redirect("source:list")
