export default function PortfolioTable({ data }) {
    return (
        <div className="overflow-x-auto">
            <table className="min-w-full bg-white">
                <thead>
                    <tr>
                        <th className="py-2 px-4 border">Symbol</th>
                        <th className="py-2 px-4 border">Quantity</th>
                        <th className="py-2 px-4 border">Price</th>
                        <th className="py-2 px-4 border">Value</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((item, index) => (
                        <tr key={index}>
                            <td className="py-2 px-4 border">{item.symbol}</td>
                            <td className="py-2 px-4 border">{item.quantity}</td>
                            <td className="py-2 px-4 border">{item.price}</td>
                            <td className="py-2 px-4 border">{item.quantity * item.price}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}