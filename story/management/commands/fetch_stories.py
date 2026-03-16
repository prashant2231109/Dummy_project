from datetime import datetime

from django.core.management.base import BaseCommand

from clients.models import Subscriber
from story.services import fetch_stories


class Command(BaseCommand):
    help = "Fetch stories for all subscribers"

    def handle(self, *args, **options):
        subscribers = Subscriber.objects.select_related("user", "company")

        if not subscribers.exists():
            self.stdout.write(self.style.WARNING("No subscribers found."))
            return

        total = 0
        for subscriber in subscribers:
            fetch_stories(subscriber.user)
            total += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"[{datetime.now()}] Fetched stories for {total} subscribers."
                )
            )
