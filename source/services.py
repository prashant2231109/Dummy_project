def create_source(form, user):
    source = form.save(commit=False)
    source.company = user.subscriber.company
    source.created_by = user
    source.updated_by = user
    source.save()
    form.save_m2m()

    return source
