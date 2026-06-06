const API_URL = 'https://student-performance-predictor-2ktw.onrender.com';

// Helper to get headers with Auth
const getAuthHeaders = () => {
    const token = localStorage.getItem('access_token');
    return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    };
};

// --- Theme Management ---
const initTheme = () => {
    const theme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', theme);
    const toggle = document.getElementById('themeToggle');
    if (toggle) {
        toggle.addEventListener('click', () => {
            const current = document.documentElement.getAttribute('data-theme');
            const target = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', target);
            localStorage.setItem('theme', target);
        });
    }
};

// --- AUTH (FIXED LOGIN) ---
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const msgDiv = document.getElementById('message');

        try {
            // ✅ FIXED: FastAPI OAuth expects x-www-form-urlencoded
            const params = new URLSearchParams();
            params.append('username', document.getElementById('username').value);
            params.append('password', document.getElementById('password').value);

            const response = await fetch(`${API_URL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: params
            });

            if (response.ok) {
                const data = await response.json();

                localStorage.setItem('access_token', data.access_token);
                window.location.href = 'dashboard.html';

            } else {
                const error = await response.json();
                msgDiv.style.display = 'block';
                msgDiv.innerText = error.detail || 'Login failed';
                msgDiv.style.color = 'var(--error)';
            }

        } catch (err) {
            console.error(err);
            msgDiv.style.display = 'block';
            msgDiv.innerText = 'Server error. Is the backend running?';
        }
    });
}

// --- SIGNUP ---
const signupForm = document.getElementById('signupForm');
if (signupForm) {
    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const msgDiv = document.getElementById('message');

        const userData = {
            username: document.getElementById('username').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value
        };

        try {
            const response = await fetch(`${API_URL}/auth/signup`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userData)
            });

            if (response.ok) {
                const data = await response.json();
                
                // --- NEW: Robust Auto-Login ---
                // If backend doesn't return a token (old version/Render), log in manually
                if (!data.access_token) {
                    const loginParams = new URLSearchParams();
                    loginParams.append('username', userData.username);
                    loginParams.append('password', userData.password);

                    const loginRes = await fetch(`${API_URL}/auth/login`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                        body: loginParams
                    });

                    if (loginRes.ok) {
                        const loginData = await loginRes.json();
                        localStorage.setItem('access_token', loginData.access_token);
                    }
                } else {
                    localStorage.setItem('access_token', data.access_token);
                }
                
                msgDiv.style.display = 'block';
                msgDiv.innerText = 'Signup successful! Logging you in...';
                msgDiv.style.color = 'var(--success)';
                
                setTimeout(() => window.location.href = 'dashboard.html', 1500);
            } else {
                const error = await response.json();
                msgDiv.style.display = 'block';
                msgDiv.innerText = error.detail || 'Signup failed';
                msgDiv.style.color = 'var(--error)';
            }

        } catch (err) {
            console.error(err);
        }
    });
}

// --- LOGOUT ---
const logoutBtn = document.getElementById('logoutBtn');
if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('access_token');
        window.location.href = 'login.html';
    });
}

// --- DASHBOARD ---
const predictionForm = document.getElementById('predictionForm');
if (predictionForm) {

    if (!localStorage.getItem('access_token')) {
        window.location.href = 'login.html';
    }

    fetch(`${API_URL}/profile/`, { headers: getAuthHeaders() })
        .then(res => {
            if (!res.ok) throw new Error('Failed to fetch profile');
            return res.json();
        })
        .then(user => {
            console.log('Profile Response:', user);
            if (user && user.username) {
                document.getElementById('userGreeting').innerText = `Hi, ${user.username}`;
            } else {
                console.warn('Username missing in profile response');
                document.getElementById('userGreeting').innerText = 'Hi!';
            }
        })
        .catch(err => {
            console.error('Profile fetch error:', err);
            document.getElementById('userGreeting').innerText = 'Welcome!';
        });

    console.log('Using API_URL:', API_URL);

    predictionForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const payload = {
            study_hours: parseFloat(document.getElementById('study_hours').value),
            attendance: parseFloat(document.getElementById('attendance').value),
            previous_score: parseFloat(document.getElementById('previous_score').value),
            assignments_completed: parseInt(document.getElementById('assignments_completed').value)
        };

        try {
            const response = await fetch(`${API_URL}/predict/`, {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                const result = await response.json();
                displayResult(result.predicted_score);
                loadHistory();
            } else if (response.status === 401) {
                window.location.href = 'login.html';
            }

        } catch (err) {
            console.error(err);
        }
    });

    const displayResult = (score) => {
        document.getElementById('noPrediction').style.display = 'none';
        document.getElementById('resultContainer').style.display = 'block';

        document.getElementById('predictedScore').innerText = score.toFixed(2);

        const msgEl = document.getElementById('predictionMessage');
        if (score >= 80) msgEl.innerText = "Excellent! Keep it up.";
        else if (score >= 60) msgEl.innerText = "Good job. Room for improvement.";
        else msgEl.innerText = "Focus more on studies and attendance.";
    };

    const loadHistory = async () => {
        try {
            const response = await fetch(`${API_URL}/predict/history`, {
                headers: getAuthHeaders()
            });

            if (response.ok) {
                const history = await response.json();
                updateHistoryTable(history);
                updateChart(history);
            }
        } catch (err) {
            console.error(err);
        }
    };

    const updateHistoryTable = (history) => {
        const tbody = document.getElementById('historyBody');
        tbody.innerHTML = '';

        history.forEach(p => {
            const date = new Date(p.created_at).toLocaleDateString();

            tbody.innerHTML += `
                <tr>
                    <td>${date}</td>
                    <td>${p.study_hours}h</td>
                    <td>${p.attendance}%</td>
                    <td>${p.previous_score}</td>
                    <td style="color: var(--primary); font-weight: 600;">
                        ${p.predicted_score.toFixed(1)}
                    </td>
                </tr>
            `;
        });
    };

    let chartInstance = null;

    const updateChart = (history) => {
        const ctx = document.getElementById('historyChart').getContext('2d');

        const data = history.slice(0, 7).reverse();
        const labels = data.map(p => new Date(p.created_at).toLocaleDateString());
        const scores = data.map(p => p.predicted_score);

        if (chartInstance) chartInstance.destroy();

        chartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels,
                datasets: [{
                    label: 'Predicted Score Trend',
                    data: scores,
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    y: { min: 0, max: 100 },
                    x: { grid: { display: false } }
                }
            }
        });
    };

    const exportBtn = document.getElementById('exportCsvBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', async () => {
            const response = await fetch(`${API_URL}/predict/export`, {
                headers: getAuthHeaders()
            });

            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);

                const a = document.createElement('a');
                a.href = url;
                a.download = 'student_prediction_history.csv';
                a.click();
            }
        });
    }

    initTheme();
    loadHistory();

} else {
    initTheme();
}
