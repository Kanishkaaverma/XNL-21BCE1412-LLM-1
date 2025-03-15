export default function ComplianceLogs({ logs }) {
    return (
        <div className="overflow-x-auto">
            <table className="min-w-full bg-white">
                <thead>
                    <tr>
                        <th className="py-2 px-4 border">Action</th>
                        <th className="py-2 px-4 border">Timestamp</th>
                        <th className="py-2 px-4 border">Details</th>
                    </tr>
                </thead>
                <tbody>
                    {logs.map((log, index) => (
                        <tr key={index}>
                            <td className="py-2 px-4 border">{log.action}</td>
                            <td className="py-2 px-4 border">{log.timestamp}</td>
                            <td className="py-2 px-4 border">{log.details}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}