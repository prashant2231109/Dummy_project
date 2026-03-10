from urllib import request

def add_story(form, user):
    story = form.save(commit=False)
    story.created_by = user
    story.updated_by = user
    story.company = user.subscriber.company
    story.save()
    form.save_m2m()

    return story



