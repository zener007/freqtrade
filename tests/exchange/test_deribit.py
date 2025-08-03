import sys
import types

from freqtrade.enums import MarginMode, TradingMode
from tests.conftest import get_patched_exchange


# Provide a minimal stub for the torch module so that tests don't require the real dependency.
torch_module = types.ModuleType("torch")
logging_module = types.ModuleType("_logging")
logging_module._init_logs = lambda: None  # type: ignore[attr-defined]
torch_module._logging = logging_module  # type: ignore[attr-defined]
sys.modules.setdefault("torch", torch_module)


def test_deribit_supports_isolated_futures(default_conf, mocker):
    default_conf["trading_mode"] = TradingMode.FUTURES
    default_conf["margin_mode"] = MarginMode.ISOLATED
    exchange = get_patched_exchange(
        mocker,
        default_conf,
        exchange="deribit",
        mock_supported_modes=False,
    )
    assert (
        TradingMode.FUTURES,
        MarginMode.ISOLATED,
    ) in exchange._supported_trading_mode_margin_pairs
    ccxt_config = exchange._ccxt_config
    assert ccxt_config.get("options", {}).get("defaultType") == "future"
