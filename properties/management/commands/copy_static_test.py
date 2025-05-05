import os
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand
from django.contrib.staticfiles import finders
from django.conf import settings


class Command(BaseCommand):
    help = 'Manually copy static files to test file system access and permissions'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Manual Static Files Copy Test ==='))
        
        # Define static files to copy
        test_files = [
            'admin/css/base.css',
            'admin/js/vendor/jquery/jquery.js',
            'jazzmin/css/main.css',
            'vendor/fontawesome-free/css/all.min.css',
            'vendor/adminlte/css/adminlte.min.css',
            'vendor/adminlte/img/AdminLTELogo.png',
            'vendor/bootstrap/js/bootstrap.min.js',
            'vendor/adminlte/js/adminlte.min.js',
        ]
        
        # Get static root
        static_root = settings.STATIC_ROOT
        self.stdout.write(f"Static root directory: {static_root}")
        
        # Ensure static root exists
        if not os.path.exists(static_root):
            try:
                os.makedirs(static_root)
                self.stdout.write(self.style.SUCCESS(f"Created static root directory: {static_root}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to create static root directory: {e}"))
                return
        
        # Count success and failures
        success_count = 0
        failure_count = 0
        
        # Process each file
        for file_path in test_files:
            self.stdout.write(self.style.NOTICE(f"\nProcessing: {file_path}"))
            
            # Find the file
            source_path = finders.find(file_path)
            if not source_path:
                self.stdout.write(self.style.ERROR(f"Could not find source file: {file_path}"))
                failure_count += 1
                continue
                
            self.stdout.write(f"Source path: {source_path}")
            
            # Prepare destination path
            dest_path = os.path.join(static_root, file_path)
            dest_dir = os.path.dirname(dest_path)
            
            self.stdout.write(f"Destination path: {dest_path}")
            self.stdout.write(f"Destination directory: {dest_dir}")
            
            # Create destination directory if it doesn't exist
            if not os.path.exists(dest_dir):
                try:
                    os.makedirs(dest_dir)
                    self.stdout.write(self.style.SUCCESS(f"Created directory: {dest_dir}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to create directory: {dest_dir} - {e}"))
                    failure_count += 1
                    continue
            
            # Copy the file
            try:
                shutil.copy2(source_path, dest_path)
                self.stdout.write(self.style.SUCCESS(f"Successfully copied to: {dest_path}"))
                
                # Verify file exists
                if os.path.exists(dest_path):
                    self.stdout.write(self.style.SUCCESS(f"Verified file exists at destination"))
                    success_count += 1
                else:
                    self.stdout.write(self.style.ERROR(f"File does not exist at destination after copy!"))
                    failure_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to copy file: {e}"))
                failure_count += 1
        
        # Summary
        self.stdout.write(self.style.SUCCESS(f"\n=== Copy Test Summary ==="))
        self.stdout.write(f"Total files processed: {len(test_files)}")
        self.stdout.write(self.style.SUCCESS(f"Successfully copied: {success_count}"))
        
        if failure_count > 0:
            self.stdout.write(self.style.ERROR(f"Failed to copy: {failure_count}"))
        else:
            self.stdout.write(self.style.SUCCESS("All files copied successfully!"))
            
        # Check if all files exist now
        self.stdout.write(self.style.SUCCESS(f"\n=== Testing Access to Copied Files ==="))
        for file_path in test_files:
            test_path = os.path.join(static_root, file_path)
            if os.path.exists(test_path):
                self.stdout.write(self.style.SUCCESS(f"File exists: {file_path}"))
            else:
                self.stdout.write(self.style.ERROR(f"File does not exist: {file_path}"))

