// API endpoints
// Use local API when running on localhost/127.0.0.1, otherwise use Render URL
const isLocal = ["localhost", "127.0.0.1"].includes(window.location.hostname);
const API_BASE = isLocal ? "" : "https://deploython2171025.onrender.com";
const CRYPTOS_ENDPOINT = `${API_BASE}/api/cryptos`;
const SCRAPE_ENDPOINT = `${API_BASE}/api/scrape-now`;

// State management
let currentData = [];
let autoRefreshInterval = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadCryptoData();
    setupEventListeners();
    startAutoRefresh();
});

// Setup event listeners
function setupEventListeners() {
    const refreshBtn = document.getElementById('refreshBtn');
    refreshBtn.addEventListener('click', handleManualRefresh);
}

// Load cryptocurrency data
async function loadCryptoData() {
    try {
        showLoading();
        
        const response = await fetch(CRYPTOS_ENDPOINT);
        const result = await response.json();
        
        if (result.success && result.data) {
            currentData = result.data;
            updateUI(result.data);
            updateLastUpdateTime(result.timestamp);
            hideLoading();
        } else {
            throw new Error(result.error || 'Failed to load data');
        }
    } catch (error) {
        console.error('Error loading crypto data:', error);
        showError(error.message);
    }
}

// Update UI with data
function updateUI(data) {
    if (!data || data.length === 0) {
        showError('No data available');
        return;
    }
    
    updateStats(data);
    updateTable(data);
    document.getElementById('tableContainer').style.display = 'block';
}

// Update statistics cards
function updateStats(data) {
    const totalCryptos = data.length;
    const gainers = data.filter(c => c.change_24h > 0).length;
    const losers = data.filter(c => c.change_24h < 0).length;
    const totalMarketCap = data.reduce((sum, c) => sum + (c.market_cap || 0), 0);
    
    document.getElementById('totalCryptos').textContent = totalCryptos;
    document.getElementById('gainers').textContent = gainers;
    document.getElementById('losers').textContent = losers;
    document.getElementById('totalMarketCap').textContent = formatCurrency(totalMarketCap);
}

// Update crypto table
function updateTable(data) {
    const tbody = document.getElementById('cryptoTableBody');
    tbody.innerHTML = '';
    
    data.forEach((crypto, index) => {
        const row = createTableRow(crypto, index + 1);
        tbody.appendChild(row);
    });
}

// Create table row for a cryptocurrency
function createTableRow(crypto, rank) {
    const tr = document.createElement('tr');
    
    const change24h = parseFloat(crypto.change_24h || 0);
    const isPositive = change24h >= 0;
    const changeClass = isPositive ? 'change-positive' : 'change-negative';
    const badgeClass = isPositive ? 'badge-positive' : 'badge-negative';
    const changeIcon = isPositive ? '▲' : '▼';
    
    tr.innerHTML = `
        <td>${rank}</td>
        <td>
            <div class="crypto-info">
                <img src="${crypto.image_url}" alt="${crypto.name}" class="crypto-icon" onerror="this.src='https://via.placeholder.com/32'">
                <div class="crypto-name">
                    <strong>${crypto.name}</strong>
                    <span class="crypto-symbol">${crypto.symbol}</span>
                </div>
            </div>
        </td>
        <td class="price">${formatCurrency(crypto.price)}</td>
        <td>
            <span class="badge ${badgeClass}">
                ${changeIcon} ${Math.abs(change24h).toFixed(2)}%
            </span>
        </td>
        <td>${formatCurrency(crypto.market_cap)}</td>
        <td>${formatCurrency(crypto.volume_24h)}</td>
        <td>${formatTimeAgo(crypto.last_updated)}</td>
    `;
    
    return tr;
}

// Handle manual refresh button
async function handleManualRefresh() {
    const btn = document.getElementById('refreshBtn');
    const originalText = btn.innerHTML;
    
    try {
        btn.disabled = true;
        btn.innerHTML = '<span class="btn-icon">⏳</span> Refreshing...';
        
        // Trigger immediate scrape
        const scrapeResponse = await fetch(SCRAPE_ENDPOINT);
        const scrapeResult = await scrapeResponse.json();
        
        if (scrapeResult.success) {
            // Wait a moment for data to be saved
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // Reload the data
            await loadCryptoData();
            
            showNotification('✅ Data refreshed successfully!');
        } else {
            throw new Error(scrapeResult.error || 'Refresh failed');
        }
    } catch (error) {
        console.error('Error refreshing data:', error);
        showNotification('❌ Failed to refresh data', 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalText;
    }
}

// Start auto-refresh
function startAutoRefresh() {
    // Refresh every 2 minutes
    autoRefreshInterval = setInterval(() => {
        console.log('Auto-refreshing data...');
        loadCryptoData();
    }, 120000); // 2 minutes
}

// Format currency
function formatCurrency(value) {
    if (!value) return '$0.00';
    
    if (value >= 1e12) {
        return `$${(value / 1e12).toFixed(2)}T`;
    } else if (value >= 1e9) {
        return `$${(value / 1e9).toFixed(2)}B`;
    } else if (value >= 1e6) {
        return `$${(value / 1e6).toFixed(2)}M`;
    } else if (value >= 1000) {
        return `$${(value / 1000).toFixed(2)}K`;
    }
    
    return `$${value.toFixed(2)}`;
}

// Format time ago
function formatTimeAgo(timestamp) {
    if (!timestamp) return 'Unknown';
    
    const date = new Date(timestamp);
    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);
    
    if (seconds < 60) return 'Just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)} min ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)} hours ago`;
    return `${Math.floor(seconds / 86400)} days ago`;
}

// Update last update time
function updateLastUpdateTime(timestamp) {
    const element = document.getElementById('lastUpdate');
    if (timestamp) {
        element.textContent = formatTimeAgo(timestamp);
    }
}

// Show loading state
function showLoading() {
    document.getElementById('loadingState').style.display = 'block';
    document.getElementById('errorState').style.display = 'none';
    document.getElementById('tableContainer').style.display = 'none';
}

// Hide loading state
function hideLoading() {
    document.getElementById('loadingState').style.display = 'none';
}

// Show error state
function showError(message) {
    document.getElementById('loadingState').style.display = 'none';
    document.getElementById('tableContainer').style.display = 'none';
    document.getElementById('errorState').style.display = 'block';
    document.getElementById('errorMessage').textContent = message;
}

// Show notification
function showNotification(message, type = 'success') {
    // Simple console notification for now
    // You can implement a toast notification system here
    console.log(`[${type.toUpperCase()}] ${message}`);
    
    // Optional: Add a temporary alert
    const alertDiv = document.createElement('div');
    alertDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        background: ${type === 'success' ? '#10b981' : '#ef4444'};
        color: white;
        border-radius: 8px;
        font-weight: 600;
        z-index: 1000;
        animation: fadeIn 0.3s ease;
    `;
    alertDiv.textContent = message;
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => alertDiv.remove(), 300);
    }, 3000);
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
});
