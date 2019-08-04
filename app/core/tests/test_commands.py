# allows us to mock the behavior of the Django get database function
# we can then simulate the database being available and then not being available
from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase

class CommandTests(TestCase):
    
    """ Going to ass a management command to the core app of our Django Project.
        This is going ot make sure that the database is available before 
        continuing and running other commands. This command is going to be used in 
        our docker-compose file when starting and running our Django app. The reason
        that we need this command is it is sometimes found that when using postgres
        with docker compose in a Django app, sometimes the Django app fails to 
        start because of a database error. This is because once the Postgres service
        has started, there are a few extra setup tasks that need to be done on the 
        Postgres before the database is ready and therefore it will fail with an 
        exception and you will need to restart the app. To improve the reliability 
        of the app, we are going to put a helper command in front of all of the 
        commands that we run in docker compose that will ensure that the database 
        is up and ready to accept connections before we try and access the database.
        This will make it more reliable both locally and as a production system.
    """

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        """ We need to simulate the behavior of Django when the database is available.
            Our management command is going to try to retrieve the database connection
            from Django and its going to check if it retrieves an OperationalError or 
            not. If it retrieves an OperationalError, then the database is not available.
            If an OperationalError is not thrown, then the database is available and 
            the command will continue. To setup our test, we're going to override
            the  behavior of the connectionHandler and we're just gonig to make it return 
            true and not throw any exception and therefore our call command or our 
            management commands should just continue and allow us to continue with the 
            execution flow. We will use the patch to mock the ConnectionHandler to just 
            return everytime it is called. 

            The patch() decorators make is easy to temporarily replace classes in a 
            particular module with a Mock object. 
        """
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1) 

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for DB"""
        """ Here we are checking that the wait_for_db command will try the database 5 times
            and on the sixth time it'll be successful and continue 
        """
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect=[OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
