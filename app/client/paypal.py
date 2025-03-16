import requests
import json
import os

from dotenv import load_dotenv

from client.models import Subscription, SubscriptionPlan
from client.exceptions import SubscriptionNotDeletedException

load_dotenv()


def get_access_token() -> str:
    """Makes request to PayPal API and returns access token."""

    data = {'grant_type': 'client_credentials'}

    headers = {
        'Content-Type': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    url = 'https://api-m.sandbox.paypal.com/v1/oauth2/token'
    client_id = os.environ.get('PAYPAL_CLIENT_ID')
    secret_id = os.environ.get('PAYPAL_SECRET_ID')

    r = requests.post(
        url,
        auth=(client_id, secret_id),
        headers=headers,
        data=data
    )
    r_content = r.json()
    access_token = r_content['access_token']

    return access_token


def cancel_subscription_paypal(access_token, sub_id):
    """Cancel subscription on PayPal side."""

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token,
        'Accept': 'application/json'
    }
    url = (f'https://api-m.sandbox.paypal.com/v1/billing/subscriptions/'
           f'{sub_id}/cancel')

    r = requests.post(url, headers=headers)

    if r.status_code == 204:
        return True

    raise SubscriptionNotDeletedException()


def update_subscription_paypal(access_token, sub_id):

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token,
        'Accept': 'application/json'
    }

    subscription = Subscription.objects.get(paypal_subscription_id=sub_id)
    current_sub_plan = subscription.subscription_plan

    if current_sub_plan.name == 'standard':
        plan = SubscriptionPlan.objects.get(name='premium')
    else:
        plan = SubscriptionPlan.objects.get(name='standard')

    new_sub_plan_id = plan.paypal_plan_id

    url = (f'https://api-m.sandbox.paypal.com/v1/billing/subscriptions/'
           f'{sub_id}/revise')
    revision_data = {'plan_id': new_sub_plan_id}

    r = requests.post(url, headers=headers, data=json.dumps(revision_data))
    r_content = r.json()

    approve_link = None

    if r.status_code == 200:
        for link in r_content.get('links', []):
            if link['rel'] == 'approve':
                approve_link = link['href']

    return approve_link
