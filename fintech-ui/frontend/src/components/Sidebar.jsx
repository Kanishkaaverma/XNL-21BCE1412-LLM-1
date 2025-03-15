import Link from 'next/link';

export default function Sidebar() {
    return (
        <div className="w-64 bg-gray-800 text-white p-4">
            <h2 className="text-xl font-bold mb-4">Menu</h2>
            <ul>
                <li className="mb-2">
                    <Link href="/dashboard" className="hover:text-blue-400">
                        Dashboard
                    </Link>
                </li>
                <li className="mb-2">
                    <Link href="/trade" className="hover:text-blue-400">
                        Trade
                    </Link>
                </li>
                <li className="mb-2">
                    <Link href="/compliance" className="hover:text-blue-400">
                        Compliance
                    </Link>
                </li>
            </ul>
        </div>
    );
}