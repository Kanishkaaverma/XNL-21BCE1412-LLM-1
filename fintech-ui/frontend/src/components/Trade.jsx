import { useState } from 'react';
import { executeTrade } from '../utils/api';

const assetSymbols = {
    stocks: ["AAPL", "GOOGL", "MSFT", "AMZN"],
    crypto: ["BTC", "ETH", "SOL", "ADA"],
    forex: ["USD/EUR", "GBP/JPY", "AUD/USD", "USD/CHF"],
};

export default function Trade() {
    const [symbol, setSymbol] = useState('');
    const [quantity, setQuantity] = useState(0);
    const [assetType, setAssetType] = useState('stocks');

    const handleTrade = async () => {
        const result = await executeTrade(assetType, symbol, quantity);
        alert(result.status);
    };

    return (
        <div className="p-4">
            <h1 className="text-2xl font-bold">Trade</h1>
            <div className="mt-4">
                <select
                    value={assetType}
                    onChange={(e) => setAssetType(e.target.value)}
                    className="p-2 border"
                >
                    <option value="stocks">Stocks</option>
                    <option value="crypto">Cryptocurrencies</option>
                    <option value="forex">Forex</option>
                </select>
                <select
                    value={symbol}
                    onChange={(e) => setSymbol(e.target.value)}
                    className="p-2 border"
                >
                    <option value="">Select Symbol</option>
                    {assetSymbols[assetType].map((sym) => (
                        <option key={sym} value={sym}>{sym}</option>
                    ))}
                </select>
                <input
                    type="number"
                    placeholder="Quantity"
                    value={quantity}
                    onChange={(e) => setQuantity(e.target.value)}
                    className="p-2 border"
                />
                <button onClick={handleTrade} className="p-2 bg-blue-600 text-white">
                    Execute Trade
                </button>
            </div>
        </div>
    );
}