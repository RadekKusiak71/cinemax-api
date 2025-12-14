from unittest.mock import patch

import pytest

from payments.events import CheckoutCompletedStrategy, StripeWebhookService

pytestmark = pytest.mark.django_db

@patch.object(CheckoutCompletedStrategy, 'handle')
def test_process_executes_strategy_handle(mock_handle):
    service = StripeWebhookService()
    event = {'type': 'checkout.session.completed', 'data': {}}
    service.process(event)
    mock_handle.assert_called_once_with(event)