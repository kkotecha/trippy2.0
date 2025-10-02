const API_URL = 'http://localhost:8000';

let currentTab = '';
let tripData = null;

// Form submission
document.getElementById('tripForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const request = {
        country: formData.get('country'),
        total_duration: parseInt(formData.get('total_duration')),
        interests: formData.get('interests').split(',').map(s => s.trim()),
        budget_tier: formData.get('budget_tier'),
        num_cities: formData.get('num_cities') ? parseInt(formData.get('num_cities')) : null,
        starting_city: formData.get('starting_city') || null,
        travel_pace: formData.get('travel_pace')
    };

    // Show loading
    document.getElementById('formContainer').classList.add('hidden');
    document.getElementById('loadingContainer').classList.remove('hidden');

    try {
        const response = await fetch(`${API_URL}/plan-trip`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(request)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Clear previous trip data completely
        tripData = null;

        tripData = await response.json();

        // Hide loading, show results
        document.getElementById('loadingContainer').classList.add('hidden');
        document.getElementById('resultsContainer').classList.remove('hidden');

        displayResults(tripData);

    } catch (error) {
        console.error('Error:', error);
        document.getElementById('loadingContainer').classList.add('hidden');
        document.getElementById('formContainer').classList.remove('hidden');
        alert('Error planning trip: ' + error.message);
    }
});

function displayResults(data) {
    const tabsContainer = document.getElementById('tabs');
    const contentContainer = document.getElementById('tabContent');

    // Force clear all previous content
    tabsContainer.innerHTML = '';
    contentContainer.innerHTML = '';

    // Clear any stored state
    currentTab = '';

    // Small delay to ensure DOM is cleared
    setTimeout(() => {
        renderAllTabs(data);
    }, 0);
}

function renderAllTabs(data) {

    // Tab 1: Journey Overview
    addTab('overview', '📍 Overview', renderOverview(data));

    // Tab 2: Route & Transport
    addTab('transport', '🚆 Transport', renderTransport(data));

    // Tab 3-N: Per-city tabs
    data.city_plans.forEach((cityPlan, index) => {
        const icons = ['🏙️', '🌆', '🌃', '🏛️', '🎎', '🏰'];
        addTab(
            `city-${index}`,
            `${icons[index % icons.length]} ${cityPlan.city_name}`,
            renderCity(cityPlan)
        );
    });

    // Budget tab
    addTab('budget', '💰 Budget', renderBudget(data.budget_summary));

    // Logistics tab
    addTab('logistics', '🎒 Logistics', renderLogistics(data.logistics));

    // Activate first tab
    activateTab('overview');
}

function addTab(id, label, content) {
    const tabsContainer = document.getElementById('tabs');
    const contentContainer = document.getElementById('tabContent');

    // Create tab button
    const tab = document.createElement('button');
    tab.id = `tab-${id}`;
    tab.className = 'px-6 py-3 font-medium text-gray-600 hover:text-blue-600 hover:bg-gray-100 whitespace-nowrap transition';
    tab.textContent = label;
    tab.onclick = () => activateTab(id);
    tabsContainer.appendChild(tab);

    // Create content div
    const contentDiv = document.createElement('div');
    contentDiv.id = `content-${id}`;
    contentDiv.className = 'hidden';
    contentDiv.innerHTML = content;
    contentContainer.appendChild(contentDiv);
}

function activateTab(id) {
    // Deactivate all tabs
    document.querySelectorAll('[id^="tab-"]').forEach(tab => {
        tab.classList.remove('border-b-2', 'border-blue-600', 'text-blue-600', 'bg-white');
        tab.classList.add('text-gray-600');
    });

    // Hide all content
    document.querySelectorAll('[id^="content-"]').forEach(content => {
        content.classList.add('hidden');
    });

    // Activate selected tab
    const selectedTab = document.getElementById(`tab-${id}`);
    selectedTab.classList.add('border-b-2', 'border-blue-600', 'text-blue-600', 'bg-white');
    selectedTab.classList.remove('text-gray-600');

    // Show selected content
    document.getElementById(`content-${id}`).classList.remove('hidden');

    currentTab = id;
}

function renderOverview(data) {
    const overview = data.journey_overview;
    return `
        <h2 class="text-3xl font-bold mb-6">${data.country} Journey Overview</h2>

        <div class="grid md:grid-cols-2 gap-6 mb-8">
            <div class="bg-blue-50 p-6 rounded-lg">
                <h3 class="font-semibold text-lg mb-2">🗺️ Your Route</h3>
                <p class="text-2xl font-bold text-blue-600">
                    ${overview.route.join(' → ')}
                </p>
            </div>

            <div class="bg-green-50 p-6 rounded-lg">
                <h3 class="font-semibold text-lg mb-2">💵 Estimated Budget</h3>
                <p class="text-2xl font-bold text-green-600">
                    ${overview.total_budget_estimate}
                </p>
            </div>
        </div>

        <div class="space-y-4">
            <div>
                <strong>Duration:</strong> ${data.total_duration} days
            </div>
            <div>
                <strong>Cities:</strong> ${data.cities_count}
            </div>
            <div>
                <strong>Travel Pace:</strong> ${overview.travel_pace}
            </div>
            <div>
                <strong>Nights per City:</strong>
                ${Object.entries(overview.nights_per_city)
                    .map(([city, nights]) => `${city} (${nights} nights)`)
                    .join(', ')}
            </div>
        </div>

        ${overview.route_rationale ? `
            <div class="mt-6 p-4 bg-gray-50 rounded-lg">
                <h4 class="font-semibold mb-2">Why This Route?</h4>
                <p class="text-gray-700">${overview.route_rationale}</p>
            </div>
        ` : ''}

        ${data.best_time_to_visit ? `
            <div class="mt-6 p-4 bg-yellow-50 rounded-lg">
                <h4 class="font-semibold mb-2">🌤️ Best Time to Visit</h4>
                <p class="text-gray-700">${data.best_time_to_visit}</p>
            </div>
        ` : ''}
    `;
}

function renderTransport(data) {
    const legs = data.transport_legs || [];

    return `
        <h2 class="text-3xl font-bold mb-6">🚆 Inter-City Transportation</h2>

        <div class="space-y-6">
            ${legs.map((leg, index) => `
                <div class="border border-gray-200 rounded-lg p-6 bg-white shadow-sm">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-xl font-bold">
                            Leg ${index + 1}: ${leg.from} → ${leg.to}
                        </h3>
                        <span class="px-4 py-2 bg-blue-100 text-blue-800 rounded-full font-medium">
                            ${leg.cost}
                        </span>
                    </div>

                    <div class="grid md:grid-cols-2 gap-4">
                        <div>
                            <p class="text-sm text-gray-600">Method</p>
                            <p class="font-semibold">${leg.method}</p>
                        </div>
                        <div>
                            <p class="text-sm text-gray-600">Duration</p>
                            <p class="font-semibold">${leg.duration}</p>
                        </div>
                    </div>

                    <div class="mt-4">
                        <p class="text-sm text-gray-600">Booking Info</p>
                        <p class="text-gray-800">${leg.booking_info}</p>
                    </div>

                    ${leg.notes ? `
                        <div class="mt-4 p-3 bg-blue-50 rounded">
                            <p class="text-sm text-blue-800">💡 ${leg.notes}</p>
                        </div>
                    ` : ''}
                </div>
            `).join('')}
        </div>
    `;
}

function renderCity(cityPlan) {
    return `
        <h2 class="text-3xl font-bold mb-2">${cityPlan.city_name}</h2>
        <p class="text-gray-600 mb-8">Staying ${cityPlan.nights} nights</p>

        <!-- Accommodation -->
        <section class="mb-12">
            <h3 class="text-2xl font-semibold mb-4">🏨 Where to Stay</h3>
            <div class="grid md:grid-cols-2 gap-4">
                ${cityPlan.accommodation.map(hotel => `
                    <div class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition">
                        <h4 class="font-bold text-lg mb-1">${hotel.name}</h4>
                        <p class="text-sm text-gray-600 mb-2">${hotel.type} • ${hotel.neighborhood}</p>
                        <p class="text-2xl font-bold text-blue-600 mb-1">${hotel.price_per_night}/night</p>
                        <p class="text-sm text-gray-500 mb-3">Total: ${hotel.total_cost}</p>
                        <p class="text-sm text-gray-700 mb-3">${hotel.why_recommended}</p>
                        <div class="flex items-center gap-2 mb-2">
                            <span class="text-yellow-500">⭐</span>
                            <span class="font-medium">${hotel.rating}</span>
                        </div>
                        <a href="${hotel.booking_link}" target="_blank"
                           class="text-blue-600 hover:underline text-sm">
                            View availability →
                        </a>
                    </div>
                `).join('')}
            </div>
        </section>

        <!-- Itinerary -->
        <section class="mb-12">
            <h3 class="text-2xl font-semibold mb-4">📅 Daily Itinerary</h3>
            ${cityPlan.itinerary.map(day => `
                <div class="mb-8 border border-gray-200 rounded-lg p-6 bg-white">
                    <h4 class="text-xl font-bold mb-4 text-blue-600">
                        Day ${day.day}: ${day.title}
                    </h4>

                    <div class="space-y-4 mb-6">
                        ${day.activities.map(activity => `
                            <div class="flex gap-4 p-3 bg-gray-50 rounded-lg">
                                <div class="flex-shrink-0">
                                    <span class="inline-block px-3 py-1 bg-blue-100 text-blue-800 rounded font-medium text-sm">
                                        ${activity.time}
                                    </span>
                                </div>
                                <div class="flex-1">
                                    <p class="font-semibold mb-1">${activity.activity}</p>
                                    <p class="text-sm text-gray-600">📍 ${activity.location}</p>
                                    <p class="text-sm text-gray-600">⏱️ ${activity.duration} • 💵 ${activity.cost}</p>
                                    ${activity.tips ? `<p class="text-sm text-blue-600 mt-1">💡 ${activity.tips}</p>` : ''}
                                </div>
                            </div>
                        `).join('')}
                    </div>

                    <div class="p-4 bg-yellow-50 rounded-lg">
                        <h5 class="font-semibold mb-2">🍽️ Meals</h5>
                        <div class="text-sm space-y-1">
                            <p><strong>Breakfast:</strong> ${day.meals.breakfast}</p>
                            <p><strong>Lunch:</strong> ${day.meals.lunch}</p>
                            <p><strong>Dinner:</strong> ${day.meals.dinner}</p>
                        </div>
                    </div>

                    <p class="mt-4 text-right font-semibold text-gray-700">
                        Daily cost: ${day.daily_cost}
                    </p>
                </div>
            `).join('')}
        </section>

        <!-- Local Transport -->
        <section>
            <h3 class="text-2xl font-semibold mb-4">🚇 Getting Around ${cityPlan.city_name}</h3>
            <div class="bg-blue-50 rounded-lg p-6">
                <div class="grid md:grid-cols-2 gap-4">
                    <div>
                        <p class="text-sm text-gray-600">Metro/Subway</p>
                        <p class="font-semibold">${cityPlan.local_transport.metro_system}</p>
                    </div>
                    <div>
                        <p class="text-sm text-gray-600">Day Pass</p>
                        <p class="font-semibold">${cityPlan.local_transport.day_pass_cost}</p>
                    </div>
                    <div>
                        <p class="text-sm text-gray-600">Taxi Apps</p>
                        <p class="font-semibold">${cityPlan.local_transport.taxi_apps.join(', ')}</p>
                    </div>
                    <div>
                        <p class="text-sm text-gray-600">Bike Rentals</p>
                        <p class="font-semibold">${cityPlan.local_transport.bike_rentals}</p>
                    </div>
                </div>
                ${cityPlan.local_transport.notes ? `
                    <p class="mt-4 text-sm text-blue-800">💡 ${cityPlan.local_transport.notes}</p>
                ` : ''}
            </div>
        </section>
    `;
}

function renderBudget(budgetSummary) {
    const breakdown = budgetSummary.breakdown;

    return `
        <h2 class="text-3xl font-bold mb-6">💰 Budget Breakdown</h2>

        <div class="mb-8 p-6 bg-green-50 rounded-lg border-2 border-green-200">
            <h3 class="text-lg font-semibold mb-2">Total Estimated Cost</h3>
            <p class="text-4xl font-bold text-green-600">$${breakdown.total}</p>
        </div>

        <div class="space-y-4 mb-8">
            ${Object.entries(breakdown).filter(([key]) => key !== 'total').map(([category, amount]) => `
                <div class="flex justify-between items-center p-4 bg-white border border-gray-200 rounded-lg">
                    <span class="font-medium capitalize">${category.replace(/_/g, ' ')}</span>
                    <span class="text-xl font-bold text-gray-700">$${amount}</span>
                </div>
            `).join('')}
        </div>

        <div class="bg-yellow-50 rounded-lg p-6">
            <h3 class="text-xl font-semibold mb-4">💡 Money-Saving Tips</h3>
            <ul class="space-y-2">
                ${budgetSummary.money_saving_tips.map(tip => `
                    <li class="flex items-start">
                        <span class="text-yellow-500 mr-2">•</span>
                        <span class="text-gray-700">${tip}</span>
                    </li>
                `).join('')}
            </ul>
        </div>
    `;
}

function renderLogistics(logistics) {
    const info = logistics.travel_info;

    return `
        <h2 class="text-3xl font-bold mb-6">🎒 Packing & Logistics</h2>

        <!-- Packing List -->
        <section class="mb-8">
            <h3 class="text-2xl font-semibold mb-4">📦 Packing List</h3>
            <div class="grid md:grid-cols-2 gap-3">
                ${logistics.packing_list.map(item => `
                    <div class="flex items-center p-3 bg-gray-50 rounded-lg">
                        <input type="checkbox" class="mr-3 h-5 w-5 text-blue-600">
                        <span>${item}</span>
                    </div>
                `).join('')}
            </div>
        </section>

        <!-- Travel Info -->
        <section class="space-y-6">
            <div class="border border-gray-200 rounded-lg p-6">
                <h4 class="font-semibold text-lg mb-2">🛂 Visa Requirements</h4>
                <p class="text-gray-700">${info.visa_requirements}</p>
            </div>

            <div class="border border-gray-200 rounded-lg p-6">
                <h4 class="font-semibold text-lg mb-2">💵 Currency</h4>
                <p class="text-gray-700">
                    <strong>${info.currency.code}</strong> (${info.currency.symbol})
                </p>
                <p class="text-sm text-gray-600 mt-2">${info.currency.notes}</p>
            </div>

            <div class="border border-gray-200 rounded-lg p-6">
                <h4 class="font-semibold text-lg mb-2">🏥 Health Precautions</h4>
                <p class="text-gray-700">${info.health_precautions}</p>
            </div>

            <div class="border border-gray-200 rounded-lg p-6">
                <h4 class="font-semibold text-lg mb-2">📱 Connectivity</h4>
                <p class="text-gray-700">${info.connectivity}</p>
            </div>

            <div class="border border-gray-200 rounded-lg p-6">
                <h4 class="font-semibold text-lg mb-2">🚨 Emergency Contacts</h4>
                <p class="text-gray-700">${info.emergency_contacts}</p>
            </div>

            <div class="border border-gray-200 rounded-lg p-6">
                <h4 class="font-semibold text-lg mb-2">🌍 Language Tips</h4>
                <p class="text-gray-700">${info.language_tips}</p>
            </div>
        </section>
    `;
}
