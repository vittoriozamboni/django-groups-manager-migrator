from migrator import models

def test_legions(command):
    command.stdout.write('  Get members')
    mars = models.Member.objects.get(first_name='Mars', last_name='Gradivus')
    sulla = models.Member.objects.get(first_name='Lucius', last_name='Sulla')
    metellus = models.Member.objects.get(first_name='Quintus', last_name='Metellus Pius')
    marius = models.Member.objects.get(first_name='Caius', last_name='Marius')
    quintus = models.Member.objects.get(first_name='Quintus', last_name='Balbo')
    archelaus = models.Member.objects.get(first_name='Archelaus', last_name='Cappadocian')

    command.stdout.write('  Get groups')
    gods = models.Group.objects.get(name='Gods')
    generals = models.Group.objects.get(name='Generals', parent=gods)
    consuls = models.Group.objects.get(name='Consuls', parent=gods)
    plebeians = models.Group.objects.get(name='Plebeians', parent=consuls)
    greeks = models.Group.objects.get(name='Greeks')

    command.stdout.write('  Get legions')
    legio_4 = models.Legion.objects.get(name='Legio IV')
    legio_5 = models.Legion.objects.get(name='Legio V')

    command.stdout.write('  Test basic permissions')
    assert sulla.has_perm('migrator.view_legion', legio_4)
    assert not sulla.has_perm('migrator.view_legion', legio_5)
    # owner - write
    assert sulla.has_perm('migrator.change_legion', legio_4)
    # owner - delete
    assert sulla.has_perm('migrator.delete_legion', legio_4)
    # group
    assert metellus.has_perm('migrator.view_legion', legio_4)
    assert metellus.has_perm('migrator.change_legion', legio_4)
    assert not metellus.has_perm('migrator.delete_legion', legio_4)

    command.stdout.write('  Test related groups permissions')
    # groups - upstream
    assert mars.has_perm('migrator.view_legion', legio_4)
    assert not mars.has_perm('migrator.change_legion', legio_4)
    assert not mars.has_perm('migrator.delete_legion', legio_4)
    # groups - downstream
    assert not quintus.has_perm('migrator.view_legion', legio_4)
    assert not quintus.has_perm('migrator.change_legion', legio_4)
    assert not quintus.has_perm('migrator.delete_legion', legio_4)
    # groups - sibling
    assert marius.has_perm('migrator.view_legion', legio_4)
    assert not marius.has_perm('migrator.change_legion', legio_4)
    assert not marius.has_perm('migrator.delete_legion', legio_4)
    # groups - other
    assert not archelaus.has_perm('migrator.view_legion', legio_4)
    assert not archelaus.has_perm('migrator.change_legion', legio_4)
    assert not archelaus.has_perm('migrator.delete_legion', legio_4)


def test_projects_and_workgroups(command):
    command.stdout.write('  Test total objects')
    assert len(models.Project.objects.all()) == 1
    assert len(models.WorkGroup.objects.all()) == 3
    assert len(models.WorkGroup.objects.filter(name__startswith='W')) == 2

    john = models.Member.objects.get(first_name='John', last_name='Boss')
    marcus = models.Member.objects.get(first_name='Marcus', last_name='Worker')
    julius = models.Member.objects.get(first_name='Julius', last_name='Backend')
    teresa = models.Member.objects.get(first_name='Teresa', last_name='Html')
    jack = models.Member.objects.get(first_name='Jack', last_name='College')

    pipeline = models.Pipeline.objects.get(name='Test Runner')

    command.stdout.write('  Test owner permissions')
    # owner
    assert marcus.has_perms(
        ['migrator.view_pipeline', 'migrator.change_pipeline',
         'migrator.delete_pipeline'], pipeline)

    command.stdout.write('  Test other groups')
    # backend group
    assert julius.has_perms(['migrator.view_pipeline', 'migrator.change_pipeline'], pipeline)
    assert not julius.has_perm('migrator.delete_pipeline', pipeline)
    # watcher group
    assert jack.has_perm('migrator.view_pipeline', pipeline)
    assert not jack.has_perm('migrator.change_pipeline', pipeline)
    assert not jack.has_perm('migrator.delete_pipeline', pipeline)
    # frontend group
    assert not teresa.has_perm('migrator.view_pipeline', pipeline)
    assert not teresa.has_perm('migrator.change_pipeline', pipeline)
    assert not teresa.has_perm('migrator.delete_pipeline', pipeline)
    # owner
    assert john.has_perms(
        ['migrator.view_pipeline', 'migrator.change_pipeline',
         'migrator.delete_pipeline'], pipeline)


def test_organizations(command):
    command.stdout.write('  Test proxy member as instance of OrganizationMember')
    organization = models.Organization.objects.get(name='Awesome Org, Inc.')
    org_members = organization.members
    assert isinstance(org_members[0], models.OrganizationMember)


def test_organizations_subclasses(command):
    command.stdout.write('  Test subclass member as instance of OrganizationMemberSubclass')
    organization = models.OrganizationSubclass.objects.get(name='Incredible Ltd')
    org_members = organization.members
    assert isinstance(org_members[0], models.OrganizationMemberSubclass)

