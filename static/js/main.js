// Global variables
let cryptoData = [];
let forexData = [];
let sentimentData = {};
let systemLogs = [];

// Main dashboard data loading function
async function loadDashboardData() {
    try {
        // Update status
        updateDataStatus('Loading...');
        
        // Load all data concurrently
        const [cryptoResponse, forexResponse, sentimentResponse, logsResponse] = await Promise.all([
            fetch('/api/crypto/latest'),
            fetch('/api/forex/latest'),
            fetch('/api/sentiment/summary'),
            fetch('/api/system/logs')
        ]);
        
        // Process responses
        const cryptoResult = await cryptoResponse.json();
        const forexResult = await forexResponse.json();
        const sentimentResult = await sentimentResponse.json();
        const logsResult = await logsResponse.json();
        
        // Update data
        if (cryptoResult.success) {
            cryptoData = cryptoResult.data;
            updateCryptoContent();
        }
        
        if (forexResult.success) {
            forexData = forexResult.data;
            updateForexContent();
        }
        
        if (sentimentResult.success) {
            sentimentData = sentimentResult.data;
            updateSentimentContent();
        }
        
        if (logsResult.success) {
            systemLogs = logsResult.data;
            updateLogsContent();
        }
        
        // Update dashboard stats
        updateDashboardStats();
        updateDataStatus('Active');
        
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        updateDataStatus('Error');
    }
}

// Update dashboard status cards
function updateDashboardStats() {
    // Update counts
    document.getElementById('cryptoCount').textContent = cryptoData.length;
    document.getElementById('forexCount').textContent = forexData.length;
    
    // Update last update time
    const now = new Date();
    document.getElementById('lastUpdate').textContent = now.toLocaleTimeString();
}

function updateDataStatus(status) {
    const statusElement = document.getElementById('dataStatus');
    statusElement.textContent = status;
    
    // Add color coding
    statusElement.className = 'card-text';
    if (status === 'Active') {
        statusElement.classList.add('text-success');
    } else if (status === 'Error') {
        statusElement.classList.add('text-danger');
    } else {
        statusElement.classList.add('text-warning');
    }
}

// Update cryptocurrency content
function updateCryptoContent() {
    const container = document.getElementById('cryptoContent');
    
    if (cryptoData.length === 0) {
        container.innerHTML = `
            <div class="alert alert-info">
                <i data-feather="info" class="me-2"></i>
                No cryptocurrency data available yet. Data collection runs every 30 minutes.
            </div>
        `;
        feather.replace();
        return;
    }
    
    let html = `
        <div class="row mb-3">
            <div class="col">
                <h6>Top Cryptocurrencies by Market Cap</h6>
            </div>
        </div>
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Symbol</th>
                        <th>Price (USD)</th>
                        <th>24h Change</th>
                        <th>Market Cap</th>
                        <th>Volume 24h</th>
                        <th>Last Updated</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    cryptoData.forEach(crypto => {
        const changeClass = crypto.price_change_percentage_24h > 0 ? 'text-success' : 'text-danger';
        const changeIcon = crypto.price_change_percentage_24h > 0 ? '↗' : '↘';
        
        html += `
            <tr>
                <td><strong>${crypto.name}</strong></td>
                <td><span class="badge bg-secondary">${crypto.symbol}</span></td>
                <td>$${formatNumber(crypto.price_usd, 2)}</td>
                <td class="${changeClass}">
                    ${changeIcon} ${formatNumber(crypto.price_change_percentage_24h, 2)}%
                    <br><small>$${formatNumber(crypto.price_change_24h, 2)}</small>
                </td>
                <td>$${formatLargeNumber(crypto.market_cap)}</td>
                <td>$${formatLargeNumber(crypto.volume_24h)}</td>
                <td><small>${formatDateTime(crypto.timestamp)}</small></td>
            </tr>
        `;
    });
    
    html += `
                </tbody>
            </table>
        </div>
    `;
    
    container.innerHTML = html;
}

// Update forex content
function updateForexContent() {
    const container = document.getElementById('forexContent');
    
    if (forexData.length === 0) {
        container.innerHTML = `
            <div class="alert alert-info">
                <i data-feather="info" class="me-2"></i>
                No forex data available yet. Data collection runs every 30 minutes.
            </div>
        `;
        feather.replace();
        return;
    }
    
    let html = `
        <div class="row mb-3">
            <div class="col">
                <h6>Major Currency Exchange Rates</h6>
            </div>
        </div>
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Currency Pair</th>
                        <th>Exchange Rate</th>
                        <th>Last Updated</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    forexData.forEach(forex => {
        html += `
            <tr>
                <td>
                    <strong>${forex.base_currency}/${forex.target_currency}</strong>
                </td>
                <td>${formatNumber(forex.exchange_rate, 4)}</td>
                <td><small>${formatDateTime(forex.timestamp)}</small></td>
            </tr>
        `;
    });
    
    html += `
                </tbody>
            </table>
        </div>
    `;
    
    container.innerHTML = html;
}

// Update sentiment analysis content
function updateSentimentContent() {
    const container = document.getElementById('sentimentContent');
    
    if (!sentimentData || (!sentimentData.crypto && !sentimentData.forex)) {
        container.innerHTML = `
            <div class="alert alert-info">
                <i data-feather="info" class="me-2"></i>
                No sentiment data available yet. Twitter analysis runs every 30 minutes.
                <br><small class="text-muted">Note: Twitter API credentials are required for sentiment analysis.</small>
            </div>
        `;
        feather.replace();
        return;
    }
    
    let html = `
        <div class="row">
            <div class="col-md-6">
                <h6>Cryptocurrency Sentiment</h6>
                <div class="card bg-dark">
                    <div class="card-body">
                        <canvas id="cryptoSentimentChart" width="400" height="300"></canvas>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <h6>Forex Sentiment</h6>
                <div class="card bg-dark">
                    <div class="card-body">
                        <canvas id="forexSentimentChart" width="400" height="300"></canvas>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
    
    // Create sentiment charts
    createSentimentChart('cryptoSentimentChart', sentimentData.crypto || {});
    createSentimentChart('forexSentimentChart', sentimentData.forex || {});
}

// Update system logs content
function updateLogsContent() {
    const container = document.getElementById('logsContent');
    
    if (systemLogs.length === 0) {
        container.innerHTML = `
            <div class="alert alert-info">
                <i data-feather="info" class="me-2"></i>
                No system logs available yet.
            </div>
        `;
        feather.replace();
        return;
    }
    
    let html = `
        <div class="table-responsive">
            <table class="table table-sm">
                <thead>
                    <tr>
                        <th>Time</th>
                        <th>Type</th>
                        <th>Component</th>
                        <th>Message</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    systemLogs.forEach(log => {
        const typeClass = log.log_type === 'error' ? 'text-danger' : log.log_type === 'warning' ? 'text-warning' : 'text-info';
        
        html += `
            <tr>
                <td><small>${formatDateTime(log.timestamp)}</small></td>
                <td><span class="badge bg-secondary ${typeClass}">${log.log_type.toUpperCase()}</span></td>
                <td><small>${log.component || 'System'}</small></td>
                <td><small>${log.message}</small></td>
            </tr>
        `;
    });
    
    html += `
                </tbody>
            </table>
        </div>
    `;
    
    container.innerHTML = html;
}

// Create sentiment chart
function createSentimentChart(canvasId, data) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    const labels = Object.keys(data);
    const counts = labels.map(label => data[label].count || 0);
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels.map(label => label.charAt(0).toUpperCase() + label.slice(1)),
            datasets: [{
                data: counts,
                backgroundColor: [
                    '#28a745', // positive - green
                    '#dc3545', // negative - red
                    '#6c757d'  // neutral - gray
                ],
                borderWidth: 2,
                borderColor: '#495057'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#adb5bd'
                    }
                }
            }
        }
    });
}

// Utility functions
function formatNumber(num, decimals = 2) {
    if (num === null || num === undefined) return 'N/A';
    return parseFloat(num).toFixed(decimals);
}

function formatLargeNumber(num) {
    if (num === null || num === undefined) return 'N/A';
    
    if (num >= 1e12) {
        return (num / 1e12).toFixed(2) + 'T';
    } else if (num >= 1e9) {
        return (num / 1e9).toFixed(2) + 'B';
    } else if (num >= 1e6) {
        return (num / 1e6).toFixed(2) + 'M';
    } else if (num >= 1e3) {
        return (num / 1e3).toFixed(2) + 'K';
    }
    return num.toFixed(2);
}

function formatDateTime(timestamp) {
    if (!timestamp) return 'N/A';
    const date = new Date(timestamp);
    return date.toLocaleString();
}

// Tab event listeners
document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('[data-bs-toggle="tab"]');
    tabButtons.forEach(button => {
        button.addEventListener('shown.bs.tab', function(event) {
            // Re-initialize feather icons when tab is shown
            setTimeout(() => {
                feather.replace();
            }, 100);
        });
    });
});
