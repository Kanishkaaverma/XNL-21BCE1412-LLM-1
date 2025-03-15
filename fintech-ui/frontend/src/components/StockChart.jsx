import { Line } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

const StockChart = ({ data }) => {
    if (!data || !data.labels || !data.prices) {
        return <div>No data available. Loading fallback data...</div>;
    }

    const chartData = {
        labels: data.labels,
        datasets: [
            {
                label: 'Stock Price',
                data: data.prices,
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false,
            },
        ],
    };

    return <Line data={chartData} />;
};

export default StockChart;