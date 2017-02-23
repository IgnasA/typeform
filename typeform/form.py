from .client import Client
from .form_response import FormResponses


class Form(Client):
    def __init__(self, api_key, form_id):
        super(Form, self).__init__(api_key=api_key)
        self.form_id = form_id

    def _request(self, method, params=None):
        path = 'form/{form_id}'.format(form_id=self.form_id)
        return super(Form, self)._request(method, path, params=params)

    def _get_params(self, **kwargs):
        params = dict()

        # Boolean params
        for name in ('completed', ):
            value = kwargs.get(name)
            if value is not None:
                params[name] = 'true' if value else 'false'

        # Number params
        for name in ('limit', 'since', 'offset', 'until'):
            value = kwargs.get(name)
            if value is not None:
                params[name] = int(value)

        # Order by
        if 'order_by' in kwargs:
            order_by = kwargs['order_by']
            if order_by is not None:
                if ',' in order_by:
                    params['order_by[]'] = order_by
                else:
                    params['order_by'] = order_by

        # Token
        if 'token' in kwargs:
            params['token'] = kwargs['token']

        return params

    def get_responses(self, token=None, completed=None, since=None, until=None, offset=None, limit=None, order_by=None):
        params = self._get_params(
            completed=completed,
            limit=limit,
            offset=offset,
            order_by=order_by,
            since=since,
            until=until,
            token=token,
        )

        resp = self._request('GET', params=params)
        return FormResponses(stats=resp.get('stats'), responses=resp.get('responses'), questions=resp.get('questions'))

    def get_response(self, token):
        responses = self.get_responses(token=token)
        if len(responses) == 1:
            return responses[0]

        # TODO: Raise exception?
        return None

    def __repr__(self):
        return 'Form(api_key={api_key!r}, form_id={form_id!r})'.format(api_key=self.api_key, form_id=self.form_id)
