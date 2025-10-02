const API_URL = 'http://localhost:8000';

// DOM Elements
const tripForm = document.getElementById('tripForm');
const formSection = document.getElementById('formSection');
const loading = document.getElementById('loading');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const newTripBtn = document.getElementById('newTripBtn');
const retryBtn = document.getElementById('retryBtn');
const submitBtn = document.getElementById('submitBtn');

// Tab functionality
const tabBtns = document.querySelectorAll('.tab-btn');
const tabPanels = document.querySelectorAll('.tab-panel');

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;

        // Remove active styles from all tabs and panels
        tabBtns.forEach(b => {
            b.classList.remove('text-blue-600', 'bg-blue-50', 'border-blue-600');
            b.classList.add('text-gray-500', 'border-transparent');
        });
        tabPanels.forEach(p => p.classList.remove('active'));

        // Add active styles to clicked tab and corresponding panel
        btn.classList.remove('text-gray-500', 'border-transparent');
        btn.classList.add('text-blue-600', 'bg-blue-50', 'border-blue-600');
        document.getElementById(tabName).classList.add('active');
    });
});

// Set initial active tab styles
if (tabBtns.length > 0) {
    tabBtns[0].classList.add('text-blue-600', 'bg-blue-50', 'border-blue-600');
}

// Form submission
tripForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(tripForm);
    const interests = formData.get('interests').split(',').map(i => i.trim());

    const tripRequest = {
        destination: formData.get('destination'),
        interests: interests,
        duration: parseInt(formData.get('duration')),
        budget: formData.get('budget')
    };

    await planTrip(tripRequest);
});

// Plan trip function
async function planTrip(tripRequest) {
    // Show loading, hide form and errors
    formSection.style.display = 'none';
    loading.style.display = 'block';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    submitBtn.disabled = true;

    try {
        const response = await fetch(`${API_URL}/plan-trip`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(tripRequest)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        displayResults(data, tripRequest);

    } catch (error) {
        console.error('Error planning trip:', error);
        showError(error.message);
    } finally {
        submitBtn.disabled = false;
    }
}

// Display results
function displayResults(data, request) {
    loading.style.display = 'none';
    resultsSection.style.display = 'block';

    // Set title
    document.getElementById('resultsTitle').textContent =
        `Your ${request.duration}-Day ${data.destination} Adventure`;

    // Debug: Log the raw content
    console.log('Raw itinerary:', data.itinerary);
    console.log('Weather info:', data.recommendations.weather_info);
    console.log('Local tips:', data.recommendations.local_tips);

    // Set itinerary
    document.getElementById('itineraryContent').innerHTML =
        formatContent(data.itinerary);

    // Set weather info
    document.getElementById('weatherContent').innerHTML =
        formatSimpleContent(data.recommendations.weather_info || 'No weather information available');

    // Set local tips
    document.getElementById('localContent').innerHTML =
        formatSimpleContent(data.recommendations.local_tips || 'No local tips available');
}

// Format content with improved design
function formatContent(content) {
    if (!content) return '<p class="text-gray-500">No content available</p>';

    let html = '';
    const lines = content.split('\n');
    let currentDay = null;
    let currentPeriod = null;

    for (let i = 0; i < lines.length; i++) {
        let line = lines[i].trim();

        if (!line || line === '---') continue;

        // Main title
        if (line.match(/^#\s+(.+)$/)) {
            const title = line.replace(/^#\s+/, '');
            html += `<h2 class="text-2xl font-bold text-gray-900 mb-6">${title}</h2>`;
        }
        // Day headers - Start a new day section
        else if (line.match(/^#{2,4}\s+(.+)$/)) {
            // Close previous day section if exists
            if (currentDay !== null) {
                html += '</div>'; // Close day-section
            }

            const dayText = line.replace(/^#{2,4}\s+/, '');
            html += `<div class="day-section">`;
            html += `<div class="day-header">${dayText}</div>`;
            currentDay = dayText;
            currentPeriod = null;
        }
        // Time period headers
        else if (line.match(/^(Morning|Afternoon|Evening|Night):?\s*/i)) {
            const period = line.replace(/:$/, '').trim();
            html += `<div class="time-period">${period.toUpperCase()}</div>`;
            currentPeriod = period;
        }
        // Check for transfer/transportation between days
        else if (line.toLowerCase().includes('get transferred') || line.toLowerCase().includes('take the ferry')) {
            // Close current day section
            if (currentDay !== null) {
                html += '</div>'; // Close day-section
                currentDay = null;
            }

            const transferText = line.replace(/^-\s*/, '').trim();
            html += `<div class="transfer-card">
                <div class="transfer-icon">🚢</div>
                <span>${transferText}</span>
            </div>`;
        }
        // Activity line (starts with -)
        else if (line.startsWith('-')) {
            line = line.substring(1).trim();

            // Parse activity with time
            const timeMatch = line.match(/^(\d+:\d+\s*(?:AM|PM)?)\s*-\s*(.+)$/i);

            if (timeMatch) {
                const [, time, rest] = timeMatch;
                const parts = rest.split(':');
                const title = parts[0].trim();
                const description = parts.slice(1).join(':').trim();

                html += `<div class="activity-item">`;
                html += `<div class="activity-time">🕐 ${time}</div>`;
                html += `<div class="activity-title">${title}</div>`;
                if (description) {
                    html += `<div class="activity-description">${description}</div>`;
                }
                html += `</div>`;
            } else {
                // Simple activity without time
                const parts = line.split(':');
                const title = parts[0].trim();
                const description = parts.slice(1).join(':').trim();

                html += `<div class="activity-item">`;
                html += `<div class="activity-title">${title}</div>`;
                if (description) {
                    html += `<div class="activity-description">${description}</div>`;
                }
                html += `</div>`;
            }
        }
        // Metadata lines with **Label:**
        else if (line.match(/^-?\s*\*\*(.+?):\*\*\s*(.+)$/)) {
            const [, label, value] = line.match(/^-?\s*\*\*(.+?):\*\*\s*(.+)$/);

            // Just append to last activity card or create info box
            html += `<div class="text-sm text-gray-600 mt-2 pl-4">
                <strong>${label}:</strong> ${value}
            </div>`;
        }
    }

    // Close the last day section if open
    if (currentDay !== null) {
        html += '</div>';
    }

    return html || '<p class="text-gray-500">No content available</p>';
}

// Format simple content (for weather, local tips, etc.)
function formatSimpleContent(content) {
    if (!content) return '<p class="text-gray-500">No content available</p>';

    let html = '';
    const lines = content.split('\n');

    for (let i = 0; i < lines.length; i++) {
        let line = lines[i].trim();

        if (!line || line === '---') continue;

        // Main section headers with ##
        if (line.match(/^#{2}\s+(.+)$/)) {
            const title = line.replace(/^#{2}\s+/, '');
            html += `<div class="day-section">`;
            html += `<div class="day-header">${title}</div>`;
        }
        // Subsection headers with ###
        else if (line.match(/^#{3}\s+(.+)$/)) {
            const subtitle = line.replace(/^#{3}\s+/, '');
            html += `<div class="activity-title mt-3">${subtitle}</div>`;
        }
        // Bullet points
        else if (line.startsWith('-')) {
            const text = line.substring(1).trim();
            html += `<div class="activity-description mb-2">• ${text}</div>`;
        }
        // Bold text
        else if (line.match(/\*\*(.+?)\*\*/)) {
            const formatted = line.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
            html += `<div class="activity-description mb-2">${formatted}</div>`;
        }
        // Regular text
        else {
            html += `<div class="activity-description mb-2">${line}</div>`;
        }
    }

    // Close any open section
    if (html.includes('day-section') && !html.endsWith('</div>')) {
        html += '</div>';
    }

    return html || '<p class="text-gray-500">No content available</p>';
}

// Show error
function showError(message) {
    loading.style.display = 'none';
    errorSection.style.display = 'block';
    document.getElementById('errorMessage').textContent =
        message || 'Unable to plan your trip. Please check your connection and try again.';
}

// Reset to form
function resetToForm() {
    formSection.style.display = 'block';
    loading.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';

    // Reset to first tab
    tabBtns.forEach((btn, index) => {
        if (index === 0) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    tabPanels.forEach((panel, index) => {
        if (index === 0) {
            panel.classList.add('active');
        } else {
            panel.classList.remove('active');
        }
    });
}

// Event listeners for buttons
newTripBtn.addEventListener('click', resetToForm);
retryBtn.addEventListener('click', resetToForm);

// Check API health on load
window.addEventListener('load', async () => {
    try {
        const response = await fetch(`${API_URL}/health`);
        if (response.ok) {
            console.log('API is healthy');
        }
    } catch (error) {
        console.warn('API may not be running:', error);
    }
});