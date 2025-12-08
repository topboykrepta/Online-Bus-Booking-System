import os
import requests
from datetime import datetime


class MpesaService:
    """Simple wrapper for Safaricom Daraja (STK Push). Requires env vars:
    MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET, MPESA_SHORTCODE, MPESA_PASSKEY

    If env vars are missing the service will run in 'simulate' mode and return
    a fake successful response for development.
    """

    def __init__(self):
        self.consumer_key = os.environ.get('MPESA_CONSUMER_KEY')
        self.consumer_secret = os.environ.get('MPESA_CONSUMER_SECRET')
        self.shortcode = os.environ.get('MPESA_SHORTCODE')
        self.passkey = os.environ.get('MPESA_PASSKEY')
        self.env = os.environ.get('MPESA_ENV', 'sandbox')

    def is_configured(self):
        return all([self.consumer_key, self.consumer_secret, self.shortcode, self.passkey])

    def _get_token(self):
        # Real implementation would call the oauth endpoint; omitted here.
        return 'SIMULATED_TOKEN'

    def stk_push(self, phone_number: str, amount: float, account_reference: str, transaction_desc: str):
        """Initiate STK Push. Returns a dict with status and checkout id.
        In simulate mode returns a fake checkout id.
        """
        if not self.is_configured():
            return {'status': 'simulated', 'checkout_id': f'SIM-{int(datetime.utcnow().timestamp())}'}

        token = self._get_token()
        # Construct payload and call Daraja STK push (not implemented live here)
        # Placeholder for real implementation
        headers = {'Authorization': f'Bearer {token}'}
        payload = {
            'BusinessShortCode': self.shortcode,
            'Password': self.passkey,
            'Timestamp': datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': amount,
            'PartyA': phone_number,
            'PartyB': self.shortcode,
            'PhoneNumber': phone_number,
            'CallBackURL': os.environ.get('MPESA_CALLBACK_URL', 'https://example.com/mpesa/callback/'),
            'AccountReference': account_reference,
            'TransactionDesc': transaction_desc,
        }
        # A real request would be made here. For now respond with simulated id.
        return {'status': 'initiated', 'checkout_id': f'CHKOUT-{int(datetime.utcnow().timestamp())}'}
