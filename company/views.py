from dal import autocomplete
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from company.forms import CompanyForm
from company.models import Company


@login_required
def add(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            company=form.save(commit=False)
            company.created_by = request.user
            company.updated_by = request.user
            company.save()

    else:
        form = CompanyForm()
    return render(request, "company/company_add.html", {"form": form})

class CompanyAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        queryset = Company.objects.only("id", "name")
        if self.q:
            queryset = queryset.filter(name__istartswith=self.q)

        return queryset[:10]