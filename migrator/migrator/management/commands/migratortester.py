from django.core.management.base import BaseCommand, CommandError
from migrator import models
import _populate as populate
import _test as test

class Command(BaseCommand):
    help = 'Manage migrator operations'

    def add_arguments(self, parser):
        parser.add_argument('operation')

    def handle(self, *args, **options):
        try:
            operation = options['operation']
        except KeyError:
            operation = args[0]

        if operation == 'start':
            self.stdout.write('Create legions')
            populate.create_legions(self)
            self.stdout.write('Create projects and workgroups')
            populate.create_projects_and_workgroups(self)
            self.stdout.write('Create organizations')
            populate.create_organizations(self)
            self.stdout.write('Create organizations (subclasses)')
            populate.create_organizations_subclasses(self)

        self.stdout.write('Test legions')
        test.test_legions(self)
        self.stdout.write('Test projects and workgroups')
        test.test_projects_and_workgroups(self)
        self.stdout.write('Test organizations')
        test.test_organizations(self)
        self.stdout.write('Test organizations (subclasses)')
        test.test_organizations_subclasses(self)
