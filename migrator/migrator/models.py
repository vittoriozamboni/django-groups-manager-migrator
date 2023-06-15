from django.db import models
from django.db.models.signals import post_save, post_delete

from mptt.models import TreeManager

from groups_manager.models import (
    Group,
    Member,
    GroupType,
    GroupMember,
    group_save,
    group_delete,
    member_save,
    member_delete,
    group_member_save,
    group_member_delete,
)

"""
Legion main example
"""


class Legion(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


"""
Football team example
"""


class TeamBudget(models.Model):
    euros = models.IntegerField()


class Match(models.Model):
    home = models.ForeignKey(Group, related_name="match_home", on_delete=models.CASCADE)
    away = models.ForeignKey(Group, related_name="match_away", on_delete=models.CASCADE)

    class Meta:
        permissions = (("play_match", "Play match"),)


"""
Group permissions example
"""


class ITObject(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        permissions = (("manage_itobject", "Manage IT Object"),)


class Newsletter(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        permissions = (("send_newsletter", "Send Newsletter"),)


"""
Signals kwargs example with subclass
"""


class ProjectGroup(Group):
    class GroupsManagerMeta:
        member_model = "migrator.ProjectGroupMember"
        group_member_model = "migrator.ProjectGroupMember"


class ProjectMember(Member):
    pass


class ProjectGroupMember(GroupMember):
    pass


def project_get_auth_models_sync_func(instance):
    return True


def project_group_save(*args, **kwargs):
    group_save(
        *args,
        get_auth_models_sync_func=project_get_auth_models_sync_func,
        prefix="PGS_",
        suffix="_Project",
        **kwargs
    )


def project_group_delete(*args, **kwargs):
    group_delete(
        *args, get_auth_models_sync_func=project_get_auth_models_sync_func, **kwargs
    )


def project_member_save(*args, **kwargs):
    member_save(
        *args,
        get_auth_models_sync_func=project_get_auth_models_sync_func,
        prefix="PGS_",
        suffix="_Project",
        **kwargs
    )


def project_member_delete(*args, **kwargs):
    member_delete(
        *args, get_auth_models_sync_func=project_get_auth_models_sync_func, **kwargs
    )


def project_group_member_save(*args, **kwargs):
    group_member_save(
        *args, get_auth_models_sync_func=project_get_auth_models_sync_func, **kwargs
    )


def project_group_member_delete(*args, **kwargs):
    group_member_delete(
        *args, get_auth_models_sync_func=project_get_auth_models_sync_func, **kwargs
    )


post_save.connect(project_group_save, sender=ProjectGroup)
post_delete.connect(project_group_delete, sender=ProjectGroup)

post_save.connect(project_member_save, sender=ProjectMember)
post_delete.connect(project_member_delete, sender=ProjectMember)

post_save.connect(project_group_member_save, sender=ProjectGroupMember)
post_delete.connect(project_group_member_delete, sender=ProjectGroupMember)


"""
Roles example
"""


class Site(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        permissions = (("sell_site", "Sell site"),)


"""
Proxy example
"""


class ProjectManager(TreeManager):
    def all(self, *args, **kwargs):
        queryset = super(ProjectManager, self).all(*args, **kwargs)
        return queryset.filter(group_type__codename="project")

    def filter(self, *args, **kwargs):
        queryset = super(ProjectManager, self).filter(*args, **kwargs)
        return queryset.filter(group_type__codename="project")


class Project(Group):
    objects = ProjectManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.group_type:
            self.group_type = GroupType.objects.get_or_create(label="Project")[0]
        super(Project, self).save(*args, **kwargs)


post_save.connect(group_save, sender=Project)
post_delete.connect(group_delete, sender=Project)


class WorkGroupManager(TreeManager):
    def all(self, *args, **kwargs):
        queryset = super(WorkGroupManager, self).all(*args, **kwargs)
        return queryset.filter(group_type__codename="workgroup")

    def filter(self, *args, **kwargs):
        queryset = super(WorkGroupManager, self).filter(*args, **kwargs)
        return queryset.filter(group_type__codename="workgroup")


class WorkGroup(Group):
    objects = WorkGroupManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.group_type:
            self.group_type = GroupType.objects.get_or_create(label="Workgroup")[0]
        super(WorkGroup, self).save(*args, **kwargs)


post_save.connect(group_save, sender=WorkGroup)
post_delete.connect(group_delete, sender=WorkGroup)


"""
Proxy Group and Member
"""


class OrganizationMember(Member):
    class Meta:
        proxy = True


post_save.connect(member_save, sender=OrganizationMember)
post_delete.connect(member_delete, sender=OrganizationMember)


class Organization(Group):
    class Meta:
        proxy = True

    class GroupsManagerMeta:
        member_model = "migrator.OrganizationMember"


post_save.connect(group_save, sender=Organization)
post_delete.connect(group_delete, sender=Organization)


class OrganizationMemberSubclass(Member):
    phone_number = models.CharField(max_length=20)


post_save.connect(member_save, sender=OrganizationMemberSubclass)
post_delete.connect(member_delete, sender=OrganizationMemberSubclass)


class OrganizationSubclass(Group):
    address = models.CharField(max_length=200)

    class GroupsManagerMeta:
        member_model = "migrator.OrganizationMemberSubclass"


post_save.connect(group_save, sender=OrganizationSubclass)
post_delete.connect(group_delete, sender=OrganizationSubclass)


class Pipeline(models.Model):
    name = models.CharField(max_length=100)
