import { useState } from 'react';
import { executeTrade } from '../utils/api';

export default function Trade() {
    const [symbol, setSymbol] = useState('');
    const [quantity, setQuantity] = useState(0);
    const [assetType, setAssetType] = useState('stocks'); // Default to stocks

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
                <input
                    type="text"
                    placeholder="Symbol"
                    value={symbol}
                    onChange={(e) => setSymbol(e.target.value)}
                    className="p-2 border"
                />
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