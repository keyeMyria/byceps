"""
:Copyright: 2006-2018 Jochen Kupperschmidt
:License: Modified BSD, see LICENSE for details.
"""

import json

from byceps.services.newsletter.models import Subscription
from byceps.services.newsletter.types import SubscriptionState

from tests.base import AbstractAppTestCase, CONFIG_FILENAME_TEST_ADMIN
from tests.helpers import assign_permissions_to_user


class NewsletterAdminTestCase(AbstractAppTestCase):

    def setUp(self):
        super().setUp(config_filename=CONFIG_FILENAME_TEST_ADMIN)

        self.admin = self.create_admin()

        self.brand = self.create_brand('example', 'Example')

        self.setup_subscribers()

    def create_admin(self):
        admin = self.create_user('Admin')

        permission_ids = {'admin.access', 'newsletter.export_subscribers'}
        assign_permissions_to_user(admin.id, 'admin', permission_ids)

        self.create_session_token(admin.id)

        return admin

    def setup_subscribers(self):
        for number, enabled, suspended, deleted, states in [
            (1, True,  False, False, [SubscriptionState.requested                             ]),
            (2, True,  False, False, [SubscriptionState.declined                              ]),
            (3, False, False, False, [SubscriptionState.requested                             ]),
            (4, True,  False, False, [SubscriptionState.declined,  SubscriptionState.requested]),
            (5, True,  False, False, [SubscriptionState.requested, SubscriptionState.declined ]),
            (6, True,  False, False, [SubscriptionState.requested                             ]),
            (7, True,  True , False, [SubscriptionState.requested                             ]),
            (8, True,  False, True , [SubscriptionState.requested                             ]),
        ]:
            user = self.create_user(
                screen_name='User-{:d}'.format(number),
                email_address='user{:03d}@example.com'.format(number),
                enabled=enabled)

            if suspended:
                user.suspended = True
                self.db.session.commit()

            if deleted:
                user.deleted = True
                self.db.session.commit()

            self.add_subscriptions(user, states)

    def test_export_subscribers(self):
        expected_data = {
            'subscribers': [
                {
                    'screen_name': 'User-1',
                    'email_address': 'user001@example.com',
                },

                # User #2 has declined a subscription, and thus should be
                # excluded.

                # User #3 is not enabled, and thus should be excluded.

                # User #4 has initially declined, but later requested a
                # subscription, so it should be included.
                {
                    'screen_name': 'User-4',
                    'email_address': 'user004@example.com',
                },

                # User #5 has initially requested, but later declined a
                # subscription, so it should be excluded.

                {
                    'screen_name': 'User-6',
                    'email_address': 'user006@example.com',
                },

                # User #7 has been suspended and should be excluded, regardless
                # of subscription state.

                # User #8 has been deleted and should be excluded, regardless
                # of subscription state.
            ],
        }

        url = '/admin/newsletter/subscriptions/{}/export'.format(self.brand.id)
        response = self.get_as_admin(url)

        assert response.status_code == 200
        assert response.content_type == 'application/json'
        data = json.loads(response.get_data().decode('utf-8'))
        assert data == expected_data

    def test_export_subscriber_email_addresses(self):
        expected_data = '\n'.join([
            'user001@example.com',
            # User #2 has declined a subscription.
            # User #3 is not enabled.
            # User #4 has initially declined, but later requested a subscription.
            'user004@example.com',
            # User #5 has initially requested, but later declined a subscription.
            'user006@example.com',
            # User #7 has been suspended, and thus should be excluded.
            # User #8 has been deleted, and thus should be excluded.
        ]).encode('utf-8')

        url = '/admin/newsletter/subscriptions/{}/export_email_addresses'.format(self.brand.id)
        response = self.get_as_admin(url)

        assert response.status_code == 200
        assert response.content_type == 'text/plain; charset=utf-8'
        assert response.mimetype == 'text/plain'
        assert response.get_data() == expected_data

    def add_subscriptions(self, user, states):
        for state in states:
            self.add_subscription(user, state)

        self.db.session.commit()

    def add_subscription(self, user, state):
        subscription = Subscription(user.id, self.brand.id, state)
        self.db.session.add(subscription)

    def get_as_admin(self, url):
        """Make a GET request as the admin and return the response."""
        with self.client(user=self.admin) as client:
            return client.get(url)
