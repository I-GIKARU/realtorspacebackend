import os
import shutil
import time
from pathlib import Path
from django.core.management.base import BaseCommand
from django.contrib.staticfiles import finders
from django.conf import settings
from django.contrib.staticfiles.finders import get_finders


class Command(BaseCommand):
    help = 'Custom implementation to collect static files from all apps'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear the static files directory before collecting',
        )
        parser.add_argument(
            '--no-input', '--noinput',
            action='store_true',
            help='Do NOT prompt the user for input of any kind',
        )

    def handle(self, *args, **options):
        self.clear = options.get('clear', False)
        self.no_input = options.get('no_input', False)
        
        self.static_root = settings.STATIC_ROOT
        self.static_dirs = settings.STATICFILES_DIRS if hasattr(settings, 'STATICFILES_DIRS') else []
        
        self.start_time = time.time()
        self.copied_files = 0
        self.skipped_files = 0
        self.processed_paths = set()  # Keep track of already processed files
        
        self.stdout.write(self.style.SUCCESS('=== Custom Static Files Collection ==='))
        self.stdout.write(f"Static root directory: {self.static_root}")
        
        # Clear static directory if requested
        if self.clear:
            self._clear_static_directory()
        
        # Ensure static root exists
        if not os.path.exists(self.static_root):
            try:
                os.makedirs(self.static_root)
                self.stdout.write(self.style.SUCCESS(f"Created static root directory: {self.static_root}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to create static root directory: {e}"))
                return
        
        # Process all finders
        self.stdout.write(self.style.NOTICE("\nCollecting static files from finders:"))
        finders_list = list(get_finders())
        
        for finder in finders_list:
            finder_name = finder.__class__.__name__
            self.stdout.write(self.style.NOTICE(f"\nProcessing finder: {finder_name}"))
            
            try:
                # Collect all files from this finder
                for path, storage in finder.list([]):
                    # Skip already processed paths
                    if path in self.processed_paths:
                        self.skipped_files += 1
                        continue
                    
                    # Get source file
                    try:
                        source_path = storage.path(path)
                        # Process the file
                        self._copy_file(source_path, path)
                        self.processed_paths.add(path)
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"  Skipping {path}: {e}"))
                        self.skipped_files += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error processing finder {finder_name}: {e}"))
        
        # Show summary
        self._show_summary()
    
    def _clear_static_directory(self):
        """Clear the static files directory if it exists."""
        if os.path.exists(self.static_root):
            if not self.no_input:
                # Ask for confirmation if --no-input is not specified
                confirm = input(f"You have requested to clear the directory '{self.static_root}'. This will DELETE ALL FILES in this location.\nAre you sure you want to do this? [y/N]: ")
                if confirm.lower() != 'y':
                    self.stdout.write("Clear cancelled.")
                    return
            
            try:
                for root, dirs, files in os.walk(self.static_root):
                    for f in files:
                        os.unlink(os.path.join(root, f))
                self.stdout.write(self.style.SUCCESS(f"Cleared static files directory: {self.static_root}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to clear static directory: {e}"))
    
    def _copy_file(self, source_path, path):
        """Copy a single file to the static files directory."""
        dest_path = os.path.join(self.static_root, path)
        dest_dir = os.path.dirname(dest_path)
        
        # Create destination directory if it doesn't exist
        if not os.path.exists(dest_dir):
            try:
                os.makedirs(dest_dir)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  Failed to create directory: {dest_dir} - {e}"))
                return False
        
        # Copy the file
        try:
            shutil.copy2(source_path, dest_path)
            self.copied_files += 1
            
            # Log every 100 files to avoid too much output
            if self.copied_files % 100 == 0:
                self.stdout.write(f"  Copied {self.copied_files} files so far...")
                
            return True
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  Failed to copy {source_path} to {dest_path}: {e}"))
            return False
    
    def _show_summary(self):
        """Show a summary of the collection process."""
        duration = time.time() - self.start_time
        
        self.stdout.write(self.style.SUCCESS(f"\n=== Collection Summary ==="))
        self.stdout.write(f"Total files copied: {self.copied_files}")
        self.stdout.write(f"Files skipped: {self.skipped_files}")
        self.stdout.write(f"Total time: {duration:.2f} seconds")
        
        # Test that some key files exist
        self.stdout.write(self.style.SUCCESS(f"\n=== Verification ==="))
        key_files = [
            'admin/css/base.css',
            'jazzmin/css/main.css',
            'vendor/fontawesome-free/css/all.min.css',
            'vendor/adminlte/css/adminlte.min.css',
        ]
        
        for file_path in key_files:
            test_path = os.path.join(self.static_root, file_path)
            if os.path.exists(test_path):
                self.stdout.write(self.style.SUCCESS(f"✓ File exists: {file_path}"))
            else:
                self.stdout.write(self.style.ERROR(f"✗ File missing: {file_path}"))
        
        self.stdout.write(self.style.SUCCESS(f"\nStatic files collection completed successfully!"))

