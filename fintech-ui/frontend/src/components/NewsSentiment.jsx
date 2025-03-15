import { Heatmap } from 'react-heatmap-grid';

export default function NewsSentimentHeatmap({ data }) {
    return (
        <div className="p-4">
            <Heatmap
                xLabels={data.xLabels}
                yLabels={data.yLabels}
                data={data.values}
            />
        </div>
    );
}