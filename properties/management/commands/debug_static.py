from django.core.management.base import BaseCommand
from django.contrib.staticfiles import finders
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Debug static files collection'

    def handle(self, *args, **options):
        self.stdout.write("\nInstalled Apps:")
        for app in settings.INSTALLED_APPS:
            self.stdout.write(f"  {app}")

        self.stdout.write("\nStatic Files Settings:")
        self.stdout.write(f"  STATIC_ROOT: {settings.STATIC_ROOT}")
        self.stdout.write(f"  STATIC_URL: {settings.STATIC_URL}")
        self.stdout.write(f"  STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
        self.stdout.write(f"  STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")

        self.stdout.write("\nStatic Files Found:")
        for finder in finders.get_finders():
            self.stdout.write(f"\nFinder: {finder.__class__.__name__}")
            try:
                for path, storage in finder.list([]):
                    self.stdout.write(f"  {path}")
                    try:
                        abs_path = storage.path(path)
                        exists = os.path.exists(abs_path)
                        self.stdout.write(f"    at: {abs_path} (exists: {exists})")
                    except NotImplementedError:
                        self.stdout.write("    (no filesystem path available)")
            except Exception as e:
                self.stdout.write(f"  Error listing files: {e}")

