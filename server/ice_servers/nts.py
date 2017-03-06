"""
Twilio API NTS token
"""

import asyncio
from functools import partial
from twilio.rest import TwilioRestClient

from server.config import TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, TWILIO_TTL

class TwilioNTS:
    """
    Twilio NTS Token Service

    Creates a new twilio NTS token once per hour.
    """
    def __init__(self, sid=None, key=None):
        """
        Constructor

        Creates a Twilio rest client, fetches a token, and creates an aiocron
        cronjob to create a new token every hour

        :param sid str: Twilio Account Sid
        :param key str: Twilio Auth Token
        """
        self.twilio_account_sid = sid or TWILIO_ACCOUNT_SID
        self.twilio_api_key = key or TWILIO_API_KEY
        self.twilio_api_secret = key or TWILIO_API_SECRET
        self.client = TwilioRestClient(request_account=self.twilio_account_sid,
                                       token=self.twilio_api_secret,
                                       account=self.twilio_api_key)

    async def fetch_token(self, ttl=None):
        """
        Fetches token from Twilio

        :param ttl - ttl in seconds or None for default of 24h
        """
        ttl = ttl or TWILIO_TTL
        if ttl is not None:
            ttl = int(ttl)
        loop = asyncio.get_event_loop()
        token = await loop.run_in_executor(None, partial(self.client.tokens.create, ttl))
        return dict(ice_servers=token.ice_servers,
                    date_created=token.date_created.isoformat(),
                    ttl=token.ttl)
