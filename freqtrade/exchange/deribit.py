"""Deribit exchange subclass"""

from __future__ import annotations

import logging

from freqtrade.enums import MarginMode, TradingMode
from freqtrade.exchange import Exchange
from freqtrade.exchange.exchange_types import FtHas


logger = logging.getLogger(__name__)


class Deribit(Exchange):
    """Deribit exchange class.

    Adds support for isolated futures trading on the Deribit exchange.
    """

    _ft_has: FtHas = {
        "ws_enabled": True,
    }

    _ft_has_futures: FtHas = {
        "stoploss_on_exchange": True,
        "stoploss_order_types": {"limit": "limit", "market": "market"},
        "stoploss_blocks_assets": False,
    }

    _supported_trading_mode_margin_pairs: list[tuple[TradingMode, MarginMode]] = [
        (TradingMode.SPOT, MarginMode.NONE),
        (TradingMode.FUTURES, MarginMode.ISOLATED),
    ]

    @property
    def _ccxt_config(self) -> dict:
        """Return ccxt configuration based on trading mode."""
        config = super()._ccxt_config
        if self.trading_mode == TradingMode.FUTURES:
            config.setdefault("options", {})
            config["options"].update({"defaultType": "future"})
        return config
