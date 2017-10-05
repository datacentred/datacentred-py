# -*- coding: utf-8 -*-
# ===============================
#      DataCentred API wrapper
# ===============================

"""
This module introduces abstractions over DataCentred entities such as Users,

Projects, Roles and Usage. It's purpose is to hide the underlying API calls
so that you can interact with DataCentred in a straightforward manner.
*Example:*
>>> from datacentredpy import datacentred
>>> account = datacentred.authorise("access_key", "secret_key")
>>> projects = account.Projectslist_projects()
>>> user = account.find_user("id")
...
"""
# Imports
from .api import DataCentredApi


class DataCentred(object):
    """docstring for ."""

    def authorise(self, access_key=None, secret_key=None):
        account = DataCentredApi(access_key, secret_key)
        return account

        if self.access_key is None:
            raise ValueError('Access Key is missing')
        if self.secret_key is None:
            raise ValueError('Secret Key is missing')


class User(DataCentred):
    """
    A user on your DataCentred account.

    Users are team members with the ability to log into your DataCentred
    account.
    All users created in your DataCented account are backed by a corresponding
    user in OpenStack's identity service (Keystone).
    """

    def create(self, params):
        new_user = DataCentredApi.Users.create(params)
        return new_user

    def all(self):
        user_list = DataCentredApi.Users.list()
        return user_list

    def find(self, id):
        user = DataCentredApi.Users.show(id)
        return user

    def update(self, id, params):
        user = DataCentredApi.Users.update(id, params)
        return user

    def destroy(self, id):
        user = DataCentredApi.Users.destroy(id)


class Project(DataCentred):
    """
    A project on your DataCentred account.

    Projects (also called "Cloud Projects" or "Tenants") are a way of grouping
    together users and resources.
    All projects created in your DataCented account are backed by a
    corresponding project in OpenStack's identity service (Keystone).
    """

    def create(self, params):
        new_project = DataCentredApi.Projects.create(params)
        return new_project

    def all(self):
        project_list = DataCentredApi.Projects.list()
        return project_list

    def find(self, id):
        project = DataCentredApi.Projects.show(id)
        return project

    def update(self, id, params):
        project = DataCentredApi.Projects.update(id, params)
        return project

    def destroy(self, id):
        DataCentredApi.Projects.destroy(id)
        return True

    def users(self, id):
        users = DataCentredApi.Projects.list_users(id)
        return users

    def add_user(self, project_id, user_id):
        DataCentredApi.Projects.add_user(project_id, user_id)
        return True

    def remove_user(self, project_id, user_id):
        DataCentredApi.Projects.remove_user(project_id, user_id)
        return True


class Role(DataCentred):
    """
    A role on your DataCentred account.

    Roles allow simple setup of user permissions via the creation of roles,
    then assigning those roles to users.
    """

    def create(self, params):
        new_role = DataCentredApi.Roles.create(params)
        return new_role

    def all(self):
        role_list = DataCentredApi.Roles.list()
        return role_list

    def find(self, id):
        role = DataCentredApi.Roles.show(id)
        return role

    def update(self, id, params):
        role = DataCentredApi.Roles.update(id, params)
        return role

    def destroy(self, id):
        DataCentredApi.Roles.destroy(id)
        return True

    def users(self, id):
        users = DataCentredApi.Roles.list_users(id)
        return users

    def add_user(self, role_id, user_id):
        DataCentredApi.Roles.add_user(role_id, user_id)
        return True

    def remove_user(self, role_id, user_id):
        DataCentredApi.Roles.remove_user(role_id, user_id)
        return True


class Usage(DataCentred):
    """
    Usage data for a given month/year.

    Data is updated every few hours for the current month.
    """

    def find(self, year, month):
        usage = DataCentredApi.Usage.show(year, month)
        return usage
