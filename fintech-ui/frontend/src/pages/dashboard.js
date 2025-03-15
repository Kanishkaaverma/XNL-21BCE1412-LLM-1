import { useEffect, useState } from 'react';
import StockChart from '../components/StockChart';
import PortfolioTable from '../components/PortfolioTable';
import { fetchPortfolio, fetchMarketSentiment } from '../utils/api';

export default function Dashboard() {
    const [portfolio, setPortfolio] = useState([]);
    const [sentiment, setSentiment] = useState({});

    useEffect(() => {
        // Fetch portfolio data
        fetchPortfolio().then((data) => {
            console.log("Portfolio Data:", data); // Log the portfolio data
            setPortfolio(data);
        });

        // Fetch market sentiment data
        fetchMarketSentiment().then((data) => {
            console.log("Market Sentiment Data:", data); // Log the sentiment data
            setSentiment(data);
        });
    }, []);

    return (
        <div className="p-4">
            <h1 className="text-2xl font-bold">Dashboard</h1>
            <div className="mt-4">
                <StockChart data={sentiment.chartData} />
            </div>
            <div className="mt-4">
                <PortfolioTable data={portfolio} />
            </div>
        </div>
    );
}