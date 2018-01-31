"""
byceps.util.instances
~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2006-2018 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""


class ReprBuilder:
    """An instance representation builder."""

    def __init__(self, instance):
        self.instance = instance
        self.attributes = []

    def add_with_lookup(self, name):
        """Add the attribute with its value looked up on the instance."""
        value = getattr(self.instance, name)
        return self.add(name, value)

    def add(self, name, value):
        """Add the attribute with the given value."""
        return self.add_custom('{}={!r}'.format(name, value))

    def add_custom(self, value):
        """Add a custom value."""
        self.attributes.append(value)
        return self

    def build(self):
        """Assemble the full textual representation."""
        class_name = type(self.instance).__name__
        attributes = ', '.join(self.attributes)
        return '<{}({})>'.format(class_name, attributes)
