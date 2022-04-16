class TradeController:
    def __init__(self, market_apis: list) -> None:
        self.market_apis = market_apis

        # TODO: interface for kucoin, and other markets (wraps around many possible markets)
        # Will control trades, and any operations that interact with wallets on markets