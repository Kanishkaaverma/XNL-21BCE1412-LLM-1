import { useState } from 'react';
import { login } from '../utils/auth';
import { useRouter } from 'next/router';

export default function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const router = useRouter();

    const handleLogin = async () => {
        const response = await login(username, password);
        if (response && response.access_token) {
            router.push('/dashboard'); // Redirect to dashboard after login
        } else {
            alert("Login failed");
        }
    };

    return (
        <div className="p-4">
            <h1 className="text-2xl font-bold">Login</h1>
            <div className="mt-4">
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="p-2 border"
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="p-2 border"
                />
                <button onClick={handleLogin} className="p-2 bg-blue-600 text-white">
                    Login
                </button>
            </div>
        </div>
    );
}