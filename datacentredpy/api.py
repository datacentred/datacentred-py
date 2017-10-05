# -*- coding: utf-8 -*-

# Imports

import requests


class DataCentredApi(object):
    """
    DataCentredApi class for API.

    Responsible for submitting requests to DataCentred and handling responses.
    """

    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key
        self.token = self.format_token(self.access_key. self.secret_key)
        self.base_url = 'https://my.datacentred.io/api'
        self.accept_type = 'application/vnd.datacentred.api+json'
        self.api_version = '1'
        self.headers = {
            'Accept': "%s; version=%s" % (self.accept_type, self.api_version),
            'Authorization': 'Token token=%s' % self.token,
            'Content-Type': 'application/json',
            'User-Agent': 'datacentred/ruby v%s' % self.api_version
                }

    # Access a resource via HTTP GET.
    #
    # @param [String] path Desired server path.
    # @raise [Errors::Error] Raised if the server returns a non 2xx error code.
    # @return [Object] Parsed server response body.
    def _get(self, path):
        url = self.base_url + path
        response = self._action('get', url)
        return self._process_response(response)

    # Access a resource via HTTP POST.
    #
    # @param [String] path Desired server path.
    # @param [Object] payload JSON serializable object.
    # @raise [Errors::Error] Raised if the server returns a non 2xx error code.
    # @return [Object] Parsed server response body.
    def _post(self, path, payload, data=None):
        url = self.base_url + path
        response = self._action('post', url)
        return self._process_response(response)

    # Access a resource via HTTP PUT.
    #
    # @param [String] path Desired server path.
    # @param [Object] payload JSON serializable object.
    # @raise [Errors::Error] Raised if the server returns a non 2xx error code.
    # @return [Object] Parsed server response body.
    def _put(self, path, payload, data=None):
        url = self.base_url + path
        response = self._action('put', url)
        return self._process_response(response)

    # Access a resource via HTTP DELETE.
    #
    # @param [String] path Desired server path.
    # @raise [Errors::Error] Raised if the server returns a non 2xx error code.
    # @return [nil] Returns nil on success.
    def _delete(self, path, payload, data=None):
        url = self.base_url + path
        response = self._action('delete', url)
        return self._process_response(response)

    def action(self, verb, path, payload=None):
        response = getattr(requests, verb)(path, payload, headers=self.headers)
        return response

    def process_response(self, response):
        pretty_response = response.json()
        print(pretty_response)
        return pretty_response

    def format_token(access_key, secret_key):
        token = access_key + ":" + secret_key
        return token


class Users(DataCentredApi):
    """RESTful API requests for the user endpoints."""

    # Create a new user.
    #
    #   POST /api/users
    #
    # @param [Hash] params User attributes.
    # @raise [Errors::UnprocessableEntity] Raised if validations fail for the
    # supplied attributes.
    # @raise [Errors::Unauthorized] Raised if credentials aren't valid.
    # @return [Hash] New user.
    def create(self, params):
        return self._post('/users', params)

    # List all available users.
    #
    #   GET /api/users
    #
    # @raise [Errors::Unauthorized] Raised if credentials aren't valid.
    # @return [[Hash]] A collection of all users on this account.
    def list(self):
        return self._get('/users')

    # Find a user by unique ID.
    #
    #   GET /api/users/82fa8de8f09102cc
    #
    # @param [String] id The unique identifier for this user.
    # @raise [Errors::NotFound] Raised if the user couldn't be found.
    # @raise [Errors::Unauthorized] Raised if credentials aren't valid.
    # @return [Hash] The user, if it exists.
    def show(self, id):
        return self._get('/users/%d' % id)

    # Update a user by unique ID.
    #
    #   PUT /api/users/82fa8de8f09102cc
    #
    # @param [String] id The unique identifier for this user.
    # @param [Hash] params User attributes.
    # @raise [Errors::UnprocessableEntity] Raised if validations fail for the
    # supplied attributes.
    # @raise [Errors::NotFound] Raised if the user couldn't be found.
    # @raise [Errors::Unauthorized] Raised if credentials aren't valid.
    # @return [Hash] The updated user.
    def update(self, id, params):
        return self._put('/users/%d' % id, params)

    # Permanently remove the specified user.
    #
    #   DELETE /api/users/82fa8de8f09102cc
    #
    # @param [String] id The unique identifier for this user.
    # @raise [Errors::NotFound] Raised if the user couldn't be found.
    # @raise [Errors::UnprocessableEntity] Raised if validations fail for the
    # specified user.
    # @raise [Errors::Unauthorized] Raised if credentials aren't valid.
    # @return [nil] Confirms the user was destroyed.
    def destroy(self, id):
        return self._delete('/users/%d' % id)


class Projects(DataCentredApi):
    """
    A project on your DataCentred account.

    Projects (also called "Cloud Projects" or "Tenants") are a way of grouping
    together users and resources.
    All projects created in your DataCented account are backed by a
    corresponding project in OpenStack's identity service (Keystone).
    """

    def create(self, params):
        return self._post('/projects', params)

    def list(self):
        return self._get('/projects')

    def show(self, id):
        return self._get('/projects/%d' % id)

    def update(self, id, params):
        return self._put('/projects/%d' % id, params)

    def destroy(self, id):
        return self._delete('/projects/%d' % id)

    def list_users(self, id):
        return self._get('/projects/%d/users' % id)

    def add_user(self, project_id, user_id):
        return self._put('/projects/%d/users/%d' % (project_id, user_id))

    def remove_user(self, project_id, user_id):
        return self._delete('/projects/%d/users/%d' % (project_id, user_id))


class Roles(DataCentredApi):
    """
    A role on your DataCentred account.

    Roles allow simple setup of user permissions via the creation of roles,
    then assigning those roles to users.
    """

    # Create a new role.
    #
    #   POST /api/roles
    #
    # @param [Hash] params Role attributes.
    # @raise [Errors::UnprocessableEntity] Raised if validations fail for the
    # supplied attributes.
    # @raise [Errors::Unauthorized] Raised if credentials aren't valid.
    # @return [Hash] New role.
    def create(self, params):
        return self._post('/roles', params)

    # List all available roles.
    #
    #   GET /api/roles
    #
    # @raise [Errors::Unauthorized] Raised if credentials aren't valid.
    # @return [[Hash]] A collection of all roles on this account.
    def list(self):
        return self._get('/roles')

    # Find a role by unique ID.
    #
    #   GET /api/roles/ea894bed9d738d9f
    #
    # @param [String] id The unique identifier for this role.
    # @raise [Errors::NotFound] Raised if the role couldn't be found.
    # @raise [Errors::Unauthorized] Raised if credentials aren't valid.
    # @return [Hash] The role, if it exists.
    def show(self, id):
        return self._get('/roles/%d' % id)

    # Update a role by unique ID.
    #
    #   PUT /api/roles/ea894bed9d738d9f
    #
    # @param [String] id The unique identifier for this role.
    # @param [Hash] params Role attributes.
    # @raise [Errors::UnprocessableEntity] Raised if validations fail for the
    # supplied attributes.
    # @raise [Errors::NotFound] Raised if the role doesn't exist.
    # @raise [Errors::Unauthorized] Raised if credentials aren't valid.
    # @return [Hash] The updated role.
    def update(self, id, params):
        return self._put('/roles/%d' % id, params)

    # Permanently remove the specified role.
    #
    #   DELETE /api/roles/ea894bed9d738d9f
    #
    # @param [String] id The unique identifier for this role.
    # @raise [Errors::NotFound] Raised if the role couldn't be found.
    # @raise [Errors::UnprocessableEntity] Raised if validations fail for the
    # specifed role.
    # @raise [Errors::Unauthorized] Raised if credentials aren't valid.
    # @return [nil] Confirms the role was destroyed.
    def destroy(self, id):
        return self._delete('/roles/%d' % id)

    # List all users assigned to this role.
    #
    #   GET /api/roles/ea894bed9d738d9f/users
    #
    # @param [String] role_id The unique identifier for this role.
    # @raise [Errors::Unauthorized] Raised if credentials aren't valid.
    # @return [[Hash]] A collection of the role's users.
    def list_users(self, id):
        return self._get('/roles/%d/users' % id)

    # Add new user to this role, giving them the associated permissions.
    #
    #   PUT /api/roles/ea894bed9d738d9f/users/82fa8de8f09102cc
    #
    # @param [String] role_id The unique identifier for this role.
    # @param [String] user_id The unique identifier for this user.
    # @raise [Errors::NotFound] Raised if the role or user couldn't be found.
    # @raise [Errors::Unauthorized] Raised if credentials aren't valid.
    # @return [nil] Confirms that user was added (or is already present).
    def add_user(self, role_id, user_id):
        return self._put('/roles/%d/users/%d' % (role_id, user_id))

    # Remove user from this role, revoking the associated permissions.
    #
    #   DELETE /api/roles/ea894bed9d738d9f/users/82fa8de8f09102cc
    #
    # @param [String] role_id The unique identifier for this role.
    # @param [String] user_id The unique identifier for this user.
    # @raise [Errors::NotFound] Raised if the role or user coundn't be found.
    # @raise [Errors::Unauthorized] Raised if credentials aren't valid.
    # @return [nil] Confirms that user was removed (or is already absent).
    def remove_user(self, role_id, user_id):
        return self._delete('/roles/%d/users/%d' % (role_id, user_id))


class Usage(DataCentredApi):
    """
    Usage data for a given month/year.

    Data is updated every few hours for the current month.
    """

    # Retrieve account usage data for a given year/month.
    #
    #   GET /api/usage/2017/9
    #
    # @param [Integer] year The year.
    # @param [Integer] month The month.
    # @raise [Errors::NotFound] Raised if no usage data found for given
    # year/month pair.
    # @raise [Errors::Unauthorized] Raised if credentials aren't valid.
    # @return [Hash] Usage for given year/month pair.
    def show(self, year, month):
        return self._get('/usage/%d/%d' % (year, month))
