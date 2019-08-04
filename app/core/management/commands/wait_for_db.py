import time

# connections can be used to check if the database is available
from django.db import connections
# Django will throw this error if the database is not available
from django.db.utils import OperationalError
# this is the class that we need to build on to create our custom command 
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Django command to pause execution until database is available"""
    
    # this is always run whenever we run this command 
    def handle(self, *args, **options):
        self.stdout.write('Waiting for Database...')
        db_conn = None
        while not db_conn:
            try: 
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1) 
        
        self.stdout.write(self.style.SUCCESS('Database available!'))