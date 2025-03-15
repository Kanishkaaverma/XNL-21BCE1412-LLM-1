import { useEffect, useState } from 'react';
import ComplianceLogs from '../components/ComplianceLogs';
import { fetchComplianceLogs } from '../utils/api';

export default function Compliance() {
    const [logs, setLogs] = useState([]);

    useEffect(() => {
        fetchComplianceLogs().then(setLogs);
    }, []);

    return (
        <div className="p-4">
            <h1 className="text-2xl font-bold">Compliance Logs</h1>
            <div className="mt-4">
                <ComplianceLogs logs={logs} />
            </div>
        </div>
    );
}