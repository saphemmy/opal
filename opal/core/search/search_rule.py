from opal.core.discoverable import DiscoverableFeature
from opal.core.exceptions import Error
from opal.utils import camelcase_to_underscore
from opal.models import Episode, deserialize_date


class SearchException(Error):
    pass


class SearchRuleField(object):
    lookup_list = None
    enum = None
    description = None
    slug = None
    display_name = None

    @classmethod
    def get_slug(klass):
        if klass.slug is not None:
            return klass.slug

        if klass.display_name is None:
            raise ValueError(
                'Must set display_name for {0}'.format(klass)
            )
        return camelcase_to_underscore(klass.display_name).replace(' ', '')

    def to_dict(self):
        return dict(
            name=self.get_slug(),
            title=self.display_name,
            type=self.field_type,
            enum=self.enum,
            lookup_list=self.lookup_list,
            description=self.description
        )

    def query(self, given_query):
        """
            takes in the full query and returns a list of episodes
        """
        raise NotImplementedError("please implement a query")


class SearchRule(DiscoverableFeature):
    module_name = "search_rule"
    fields = []

    def get_fields(self):
        return self.fields

    def to_dict(self):
        return dict(
            name=self.get_slug(),
            display_name=self.display_name,
            advanced_searchable=True,
            fields=[i().to_dict() for i in self.get_fields()]
        )

    @classmethod
    def get(klass, name):
        """
        Return a specific subclass by slug
        """
        for sub in klass.list():
            if sub.get_slug() == name:
                return sub

    def query(self, given_query):
        given_field = given_query['field']
        query_field = next(
            f for f in self.get_fields() if f.get_slug() == given_field
        )
        return query_field().query(given_query)
