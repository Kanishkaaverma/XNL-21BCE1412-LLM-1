import Link from 'next/link';

export default function Home() {
    return (
        <div className="p-4">
            <h1 className="text-2xl font-bold">Welcome to FinTech LLM</h1>
            <Link href="/dashboard" className="text-blue-600 hover:underline">
                Go to Dashboard
            </Link>
        </div>
    );
}