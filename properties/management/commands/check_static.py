import os
from django.core.management.base import BaseCommand
from django.contrib.staticfiles import finders
from django.conf import settings
from django.contrib.staticfiles.finders import get_finders


class Command(BaseCommand):
    help = 'Check static files configuration and list findable static files'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Django Static Files Configuration ==='))
        
        # 1. Print all configured static file finders
        self.stdout.write(self.style.NOTICE('\n1. Configured static file finders:'))
        finders_list = list(get_finders())
        for finder in finders_list:
            self.stdout.write(f'  - {finder.__class__.__name__}')
        
        # 2. Print STATICFILES_DIRS setting
        self.stdout.write(self.style.NOTICE('\n2. STATICFILES_DIRS:'))
        if hasattr(settings, 'STATICFILES_DIRS'):
            for directory in settings.STATICFILES_DIRS:
                self.stdout.write(f'  - {directory}')
                if os.path.exists(directory):
                    self.stdout.write(self.style.SUCCESS(f'    Directory exists: YES'))
                else:
                    self.stdout.write(self.style.ERROR(f'    Directory exists: NO'))
        else:
            self.stdout.write(self.style.ERROR('  STATICFILES_DIRS not configured'))

        # 3. Print STATIC_ROOT setting
        self.stdout.write(self.style.NOTICE('\n3. STATIC_ROOT:'))
        if hasattr(settings, 'STATIC_ROOT'):
            self.stdout.write(f'  - {settings.STATIC_ROOT}')
            if os.path.exists(settings.STATIC_ROOT):
                self.stdout.write(self.style.SUCCESS(f'    Directory exists: YES'))
            else:
                self.stdout.write(self.style.ERROR(f'    Directory exists: NO'))
        else:
            self.stdout.write(self.style.ERROR('  STATIC_ROOT not configured'))
            
        # 4. Try to find some known static files
        self.stdout.write(self.style.NOTICE('\n4. Testing known static files:'))
        test_files = [
            'admin/css/base.css',
            'admin/js/vendor/jquery/jquery.js',
            'jazzmin/css/main.css',
            'vendor/fontawesome-free/css/all.min.css',
            'vendor/adminlte/css/adminlte.min.css',
        ]
        
        for file_path in test_files:
            found_path = finders.find(file_path)
            if found_path:
                self.stdout.write(self.style.SUCCESS(f'  Found {file_path} at {found_path}'))
            else:
                self.stdout.write(self.style.ERROR(f'  Could not find {file_path}'))
                
        # 5. List first 10 findable static files from each finder
        self.stdout.write(self.style.NOTICE('\n5. Sample of findable static files:'))
        
        for finder in finders_list:
            finder_name = finder.__class__.__name__
            self.stdout.write(self.style.SUCCESS(f'\n  Files from {finder_name}:'))
            
            try:
                count = 0
                for path, storage in finder.list([]):
                    if count < 10:  # Limit to 10 files per finder to avoid overwhelming output
                        self.stdout.write(f'    - {path}')
                        count += 1
                    else:
                        self.stdout.write(f'    ... and more (showing only first 10)')
                        break
                        
                if count == 0:
                    self.stdout.write(self.style.WARNING(f'    No files found with this finder'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'    Error listing files: {str(e)}'))

