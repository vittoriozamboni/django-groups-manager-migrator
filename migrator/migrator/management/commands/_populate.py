from migrator import models

def create_legions(command):
    command.stdout.write('  # default')

    command.stdout.write('  Create groups')
    gods = models.Group.objects.create(name='Gods')
    generals = models.Group.objects.create(name='Generals', parent=gods)
    consuls = models.Group.objects.create(name='Consuls', parent=gods)
    plebeians = models.Group.objects.create(name='Plebeians', parent=consuls)
    greeks = models.Group.objects.create(name='Greeks')

    command.stdout.write('  Create members')
    mars = models.Member.objects.create(first_name='Mars', last_name='Gradivus')
    sulla = models.Member.objects.create(first_name='Lucius', last_name='Sulla')
    metellus = models.Member.objects.create(first_name='Quintus', last_name='Metellus Pius')
    marius = models.Member.objects.create(first_name='Caius', last_name='Marius')
    quintus = models.Member.objects.create(first_name='Quintus', last_name='Balbo')
    archelaus = models.Member.objects.create(first_name='Archelaus', last_name='Cappadocian')

    command.stdout.write('  Create memberships')
    models.GroupMember.objects.create(group=gods, member=mars)
    sulla_consuls = models.GroupMember.objects.create(group=consuls, member=sulla)
    models.GroupMember.objects.create(group=consuls, member=metellus)
    models.GroupMember.objects.create(group=generals, member=marius)
    models.GroupMember.objects.create(group=plebeians, member=quintus)
    models.GroupMember.objects.create(group=greeks, member=archelaus)

    command.stdout.write('  Create legions')
    legio_4 = models.Legion.objects.create(name='Legio IV')
    models.Legion.objects.create(name='Legio V')

    command.stdout.write('  Assign legions')
    sulla_consuls.assign_object(legio_4)


def create_projects_and_workgroups(command):
    command.stdout.write('  # proxy')

    command.stdout.write('  Create groups')
    project_main = models.Project.objects.create(name='Workgroups Main Project')
    django_backend = models.WorkGroup.objects.create(name='WorkGroup Backend', parent=project_main)
    django_backend_watchers = models.WorkGroup.objects.create(name='Backend Watchers', parent=django_backend)
    django_frontend = models.WorkGroup.objects.create(name='WorkGroup FrontEnd', parent=project_main)

    command.stdout.write('  Create members')
    john = models.Member.objects.create(first_name='John', last_name='Boss')
    marcus = models.Member.objects.create(first_name='Marcus', last_name='Worker')
    julius = models.Member.objects.create(first_name='Julius', last_name='Backend')
    teresa = models.Member.objects.create(first_name='Teresa', last_name='Html')
    jack = models.Member.objects.create(first_name='Jack', last_name='College')

    command.stdout.write('  Create memberships')
    project_main.add_member(john)
    django_frontend.add_member(teresa)
    django_backend.add_member(marcus)
    django_backend.add_member(julius)
    django_backend_watchers.add_member(jack)

    command.stdout.write('  Assign pipeline with custom permission')
    pipeline = models.Pipeline.objects.create(name='Test Runner')
    custom_permissions = {
        'owner': ['view', 'change', 'delete'],
        'group': ['view', 'change'],
        'groups_upstream': ['view', 'change', 'delete'],
        'groups_downstream': ['view'],
        'groups_siblings': [],
    }
    marcus.assign_object(django_backend, pipeline, custom_permissions=custom_permissions)


def create_organizations(command):
    command.stdout.write('  # proxy with custom member')

    command.stdout.write('  Create groups')
    organization = models.Organization.objects.create(name='Awesome Org, Inc.')

    command.stdout.write('  Create members')
    john_boss = models.OrganizationMember.objects.create(first_name='Johnny', last_name='Boss')

    command.stdout.write('  Create memberships')
    organization.add_member(john_boss)


def create_organizations_subclasses(command):
    command.stdout.write('  # subclass with custom member')

    command.stdout.write('  Create groups')
    organization = models.OrganizationSubclass.objects.create(
        name='Incredible Ltd', address='First Street')

    command.stdout.write('  Create members')
    john_boss = models.OrganizationMemberSubclass.objects.create(
        first_name='Jorge', last_name='Portuguese', phone_number='033 32 33 34')

    command.stdout.write('  Create memberships')
    organization.add_member(john_boss)
