from requests.models import Response

from typing import Optional
import hmac
import hashlib
from urllib.parse import urlencode

from medici.interfaces.exchanges.interface import iCBE
from medici.decorators.permission.decorator import permission


class BinanceUSDTmExchange(iCBE):
    _E = 'https://fapi.binance.com'
    _ping = '/fapi/v1/ping'

    def __signature(self, params: dict):
        return hmac.new(self.secret.encode('utf-8'), urlencode(params).replace('%40', '@').encode('utf-8'), hashlib.sha256).hexdigest()

    def __header(self):
        return {'X-MBX-APIKEY': self.api}

    def aggTrades(
            self,
            symbol: str,
            fromId: Optional[int] = None,
            startTime: Optional[int] = None,
            endTime: Optional[int] = None,
            limit: Optional[int] = None
    ) -> Response:
        params: dict = {
            'symbol': symbol,
            'fromId': fromId,
            'startTime': startTime,
            'endTime': endTime,
            'limit': limit
        }
        r = self._r(method='get', url='/fapi/v1/aggTrades', params=params)
        assert isinstance(r, Response)
        return r

    @permission
    def account(
            self,
            timestamp: int,
            recvWindow: Optional[int] = None
    ) -> Response:
        params: dict = {'timestamp': timestamp} if recvWindow is None else {'timestamp': timestamp, 'recvWindow': recvWindow}
        params.update({'signature': self.__signature(params)})

        r = self._r(
            method='get',
            url='/fapi/v2/account',
            params=params,
            headers=self.__header()
        )
        assert isinstance(r, Response)
        return r

    @permission
    def positionRisk(
            self,
            timestamp: int,
            symbol: Optional[str] = None,
            recvWindow: Optional[int] = None
    ) -> Response:
        params: dict = {'timestamp': timestamp}
        if symbol:
            params.update({'symbol': symbol})
        if recvWindow:
            params.update({'recvWindow': recvWindow})
        params.update({'signature': self.__signature(params)})

        r = self._r(
            method='get',
            url='/fapi/v2/positionRisk',
            params=params,
            headers=self.__header()
        )
        assert isinstance(r, Response)
        return r
