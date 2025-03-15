export const login = async (username, password) => {
    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
        });
        const data = await response.json();
        if (data.access_token) {
            localStorage.setItem('token', data.access_token); // Store the token
        }
        return data;
    } catch (error) {
        console.error("Error during login:", error);
        return null;
    }
};

export const getCurrentUser = async () => {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/api/auth/me', {
            headers: { Authorization: `Bearer ${token}` },
        });
        return response.json();
    } catch (error) {
        console.error("Error fetching current user:", error);
        return null;
    }
};