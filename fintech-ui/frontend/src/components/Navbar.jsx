import Link from 'next/link';

export default function Navbar() {
    return (
        <nav className="bg-blue-600 p-4">
            <div className="container mx-auto flex justify-between items-center">
                <Link href="/" className="text-white text-2xl font-bold">
                    FinTech LLM
                </Link>
                <div className="space-x-4">
                    <Link href="/dashboard" className="text-white">
                        Dashboard
                    </Link>
                    <Link href="/trade" className="text-white">
                        Trade
                    </Link>
                    <Link href="/compliance" className="text-white">
                        Compliance
                    </Link>
                </div>
            </div>
        </nav>
    );
}