// ═══════════════════════════════════════════════════════════════════
//  EcoNews — Frontend Script (Connected to FastAPI Backend)
// ═══════════════════════════════════════════════════════════════════

const API_BASE = window.location.origin; // Same origin as the server

// ─── STATE ──────────────────────────────────────────────────────────
let allNews = {};          // { satire: [...], ai: [...], ... }
let recommendedNews = [];  // 6 sidebar recommended items
let activeCategory = 'satire';
let audioUrl = null;
let isAudioPlaying = false;

// Category labels for display
const CATEGORY_LABELS = {
    satire: 'Satire',
    ai: 'AI Technology',
    worldwide: 'Worldwide News',
    warming: 'Warming & Emotions',
    market: 'Market News',
};

// Gradient classes for sidebar items
const GRADIENT_CLASSES = [
    'gradient-bg-1', 'gradient-bg-2', 'gradient-bg-3',
    'gradient-bg-4', 'gradient-bg-5'
];


// ─── INIT ───────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    initParallax();
    initAudioPlayer();
    initEmailPopup();
    initCoffeeToast();    // ☕ shows after 15s
    initNavButtons();     // new 3-button nav
    initCategoryTabs();   // category tabs still work below the headline
    initNavAlert();       // 🔴 sad alert banner

    // Fetch everything from the backend
    fetchAllNews();
    fetchFeaturedArticle();
    fetchAudioUrl();
});


// ─── NAV ALERT DISMISS ──────────────────────────────────────────────
function initNavAlert() {
    const alert = document.getElementById('nav-alert');
    const closeBtn = document.getElementById('nav-alert-close');
    if (!alert || !closeBtn) return;

    closeBtn.addEventListener('click', () => {
        alert.classList.add('dismissed');
        setTimeout(() => alert.remove(), 350);
    });
}



// ─── COFFEE TOAST ───────────────────────────────────────────────────
function initCoffeeToast() {
    const toast = document.getElementById('coffee-toast');
    const closeBtn = document.getElementById('coffee-toast-close');
    const listenBtn = document.getElementById('coffee-listen-btn');
    const audioPlayBtn = document.getElementById('audio-headphone-btn');

    if (!toast) return;

    // Show after 15 seconds
    setTimeout(() => {
        toast.classList.remove('hidden');
        // Slight delay so CSS transition fires
        requestAnimationFrame(() => {
            requestAnimationFrame(() => toast.classList.add('show'));
        });
    }, 15000);

    // Close button — slide back down
    closeBtn.addEventListener('click', () => {
        toast.classList.remove('show');
        setTimeout(() => toast.classList.add('hidden'), 500);
    });

    // "Listen Now" — trigger audio player & close toast
    listenBtn.addEventListener('click', () => {
        if (audioPlayBtn) audioPlayBtn.click();
        toast.classList.remove('show');
        setTimeout(() => toast.classList.add('hidden'), 500);
    });
}



// ─── FETCH ALL NEWS ─────────────────────────────────────────────────
async function fetchAllNews() {
    try {
        const res = await fetch(`${API_BASE}/api/news`);
        const data = await res.json();

        allNews = data.categories || {};
        recommendedNews = data.recommended || [];
        audioUrl = data.audio_url || null;

        // Paint current category
        renderCategoryCards(activeCategory);
        renderSidebar();

    } catch (err) {
        console.error('Failed to fetch news:', err);
        showFallbackCards();
    }
}


// ─── FETCH FEATURED ARTICLE ────────────────────────────────────────
async function fetchFeaturedArticle() {
    try {
        const res = await fetch(`${API_BASE}/api/news/featured`);
        const data = await res.json();

        const headline = document.getElementById('featured-headline');
        const link = document.getElementById('featured-link');
        const meta = document.getElementById('featured-meta');
        const tagsEl = document.getElementById('featured-tags');
        const readBtn = document.getElementById('featured-read-btn');

        if (link) {
            link.textContent = data.title || 'Welcome to EcoNews';
            link.href = data.url || '#';
        } else if (headline) {
            headline.textContent = data.title || 'Welcome to EcoNews';
        }

        if (meta) meta.textContent = data.meta || '';

        if (tagsEl) {
            tagsEl.innerHTML = '';
            (data.tags || []).forEach(tag => {
                const span = document.createElement('span');
                span.textContent = `#${tag}`;
                tagsEl.appendChild(span);
            });
        }

        if (readBtn) readBtn.href = data.url || '#';

    } catch (err) {
        console.error('Failed to fetch featured article:', err);
    }
}


// ─── FETCH AUDIO URL ────────────────────────────────────────────────
async function fetchAudioUrl() {
    try {
        const res = await fetch(`${API_BASE}/api/audio`);
        const data = await res.json();
        audioUrl = data.audio_url || data.local_audio || null;

        if (audioUrl) {
            const audioEl = document.getElementById('hidden-audio');
            if (audioEl) audioEl.src = audioUrl;
        }
    } catch (err) {
        console.error('Failed to fetch audio:', err);
    }
}


// ─── RENDER CATEGORY CARDS ──────────────────────────────────────────
function renderCategoryCards(category) {
    const container = document.getElementById('dynamic-cards-container');
    if (!container) return;

    const items = allNews[category] || [];

    // Fade out
    container.classList.add('fade-out');

    setTimeout(() => {
        container.innerHTML = '';

        if (items.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <p>No news available for <strong>${CATEGORY_LABELS[category] || category}</strong> yet.</p>
                    <p class="empty-sub">Run the pipeline to curate fresh news.</p>
                </div>
            `;
            container.classList.remove('fade-out');
            return;
        }

        items.forEach((item, idx) => {
            const card = document.createElement('article');
            card.className = 'mini-card';
            card.style.animationDelay = `${idx * 0.08}s`;
            card.classList.add('card-enter');

            const tags = (item.tags || []).map(t => `<span class="card-tag">#${t}</span>`).join('');
            const source = item.source_id || '';
            const categoryLabel = CATEGORY_LABELS[category] || category;

            card.innerHTML = `
                <div class="card-gradient-bar ${GRADIENT_CLASSES[idx % GRADIENT_CLASSES.length]}"></div>
                <div class="meta">${categoryLabel} • ${source}</div>
                <h4 class="title">
                    <a href="${item.url || '#'}" target="_blank" rel="noopener">${item.title || 'Untitled'}</a>
                </h4>
                <p class="card-why">${item.why_pick || ''}</p>
                <div class="card-tags">${tags}</div>
            `;

            card.addEventListener('click', (e) => {
                if (e.target.tagName !== 'A') {
                    window.open(item.url || '#', '_blank');
                }
            });

            container.appendChild(card);
        });

        container.classList.remove('fade-out');
    }, 300);
}


// ─── RENDER SIDEBAR ─────────────────────────────────────────────────
function renderSidebar() {
    // Use the dedicated recommended items (6 items from API)
    const items = recommendedNews.length > 0 ? recommendedNews : [];

    // If no recommended, try to gather from categories
    if (items.length === 0) {
        for (const cat of Object.keys(allNews)) {
            for (const item of (allNews[cat] || [])) {
                items.push({ ...item, _category: cat });
            }
        }
    }

    // Sidebar featured (first recommended item)
    const featuredMeta = document.getElementById('sidebar-featured-meta');
    const featuredTitle = document.getElementById('sidebar-featured-title');
    const featuredCard = document.getElementById('sidebar-featured');

    if (items.length > 0) {
        const first = items[0];
        const catKey = first.category || first._category || '';
        if (featuredMeta) featuredMeta.textContent = `${CATEGORY_LABELS[catKey] || catKey} • Today`;
        if (featuredTitle) featuredTitle.textContent = first.title || 'No Title';
        if (featuredCard) {
            featuredCard.style.cursor = 'pointer';
            featuredCard.onclick = () => window.open(first.url || '#', '_blank');
        }
    }

    // Sidebar list (next 5 recommended items)
    const listContainer = document.getElementById('sidebar-list');
    if (!listContainer) return;
    listContainer.innerHTML = '';

    const sidebarItems = items.slice(1, 6);
    sidebarItems.forEach((item, idx) => {
        const article = document.createElement('article');
        article.className = 'list-item';
        article.style.cursor = 'pointer';

        const catKey = item.category || item._category || '';
        const catLabel = CATEGORY_LABELS[catKey] || catKey;

        article.innerHTML = `
            <div class="mock-thumb ${GRADIENT_CLASSES[(idx + 1) % GRADIENT_CLASSES.length]}"></div>
            <div class="item-details">
                <div class="meta">${catLabel} • Today</div>
                <h4 class="title">${item.title || 'Untitled'}</h4>
            </div>
        `;

        article.addEventListener('click', () => {
            window.open(item.url || '#', '_blank');
        });

        listContainer.appendChild(article);
    });
}


// ─── FALLBACK if API fails ──────────────────────────────────────────
function showFallbackCards() {
    const container = document.getElementById('dynamic-cards-container');
    if (!container) return;
    container.innerHTML = `
        <div class="empty-state">
            <p>Could not connect to the news server.</p>
            <p class="empty-sub">Make sure the backend is running on the same port.</p>
        </div>
    `;
}


// ─── CATEGORY TABS ──────────────────────────────────────────────────
function initCategoryTabs() {
    const tabsContainer = document.getElementById('category-tabs');
    if (!tabsContainer) return;

    tabsContainer.addEventListener('click', (e) => {
        const btn = e.target.closest('.tab-btn');
        if (!btn) return;

        const category = btn.dataset.category;
        if (!category || category === activeCategory) return;

        // Update active tab
        tabsContainer.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Update active nav link too
        const navLinks = document.getElementById('nav-links');
        if (navLinks) {
            navLinks.querySelectorAll('a').forEach(a => {
                a.classList.toggle('active', a.dataset.category === category);
            });
        }

        activeCategory = category;
        renderCategoryCards(category);
    });
}


// ─── NAV BUTTONS ─────────────────────────────────────────────────────
function initNavButtons() {
    // "Get News on Email" — opens the subscription popup
    const navEmail = document.getElementById('nav-email');
    const emailPopup = document.getElementById('email-popup');
    if (navEmail && emailPopup) {
        navEmail.addEventListener('click', (e) => {
            e.preventDefault();
            emailPopup.classList.remove('hidden');
        });
    }

    // "Voice Assistant" — triggers the audio player headphone button
    const navVoice = document.getElementById('nav-voice');
    const audioPlayBtn = document.getElementById('audio-headphone-btn');
    if (navVoice && audioPlayBtn) {
        navVoice.addEventListener('click', (e) => {
            e.preventDefault();
            audioPlayBtn.click();
        });
    }
    // "About Me" needs no JS — it uses href directly in HTML
}


// ─── AUDIO PLAYER ───────────────────────────────────────────────────
function initAudioPlayer() {
    const audioPlayer = document.getElementById('audio-player');
    const audioPlayBtn = document.getElementById('audio-headphone-btn');
    const audioStopBtn = document.getElementById('audio-stop-btn');
    const hiddenAudio = document.getElementById('hidden-audio');

    if (!audioPlayBtn || !audioStopBtn || !hiddenAudio) return;

    audioPlayBtn.addEventListener('click', async () => {
        if (isAudioPlaying) return;

        // Fetch audio URL if not loaded
        if (!audioUrl) {
            try {
                const res = await fetch(`${API_BASE}/api/audio`);
                const data = await res.json();
                audioUrl = data.audio_url || data.local_audio || null;
            } catch (err) {
                console.error('Audio fetch failed:', err);
            }
        }

        if (!audioUrl) {
            alert('No audio available yet. Run the pipeline (run_daily.py) to generate audio.');
            return;
        }

        hiddenAudio.src = audioUrl;
        hiddenAudio.play().then(() => {
            isAudioPlaying = true;
            audioPlayer.classList.add('playing');
        }).catch(err => {
            console.error('Audio play failed:', err);
            alert('Could not play audio. It may still be generating.');
        });
    });

    audioStopBtn.addEventListener('click', () => {
        hiddenAudio.pause();
        hiddenAudio.currentTime = 0;
        isAudioPlaying = false;
        audioPlayer.classList.remove('playing');
    });

    // When audio ends naturally
    hiddenAudio.addEventListener('ended', () => {
        isAudioPlaying = false;
        audioPlayer.classList.remove('playing');
    });
}


// ─── EMAIL SUBSCRIPTION POPUP ───────────────────────────────────────
function initEmailPopup() {
    const emailPopup = document.getElementById('email-popup');
    const closePopupBtn = document.getElementById('close-popup');
    const subscribeForm = document.getElementById('subscribe-form');
    const statusEl = document.getElementById('toast-status');

    // Show popup after 4 seconds
    setTimeout(() => {
        emailPopup.classList.remove('hidden');
    }, 4000);

    // Close popup on X click
    closePopupBtn.addEventListener('click', () => {
        emailPopup.classList.add('hidden');
    });

    // Handle form submission → POST to backend
    subscribeForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const emailInput = document.getElementById('subscribe-email');
        const email = emailInput.value.trim();
        const btn = subscribeForm.querySelector('.subscribe-btn');

        if (!email) return;

        btn.disabled = true;
        btn.textContent = 'Subscribing...';

        try {
            const res = await fetch(`${API_BASE}/api/subscribe`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email }),
            });

            const data = await res.json();

            if (res.ok) {
                btn.textContent = 'Subscribed! 🎉';
                btn.style.backgroundColor = '#31A572';
                if (statusEl) {
                    statusEl.textContent = `✅ ${email} subscribed successfully!`;
                    statusEl.style.color = '#31A572';
                }

                setTimeout(() => {
                    emailPopup.classList.add('hidden');
                    btn.textContent = 'Subscribe';
                    btn.style.backgroundColor = '';
                    btn.disabled = false;
                    emailInput.value = '';
                    if (statusEl) statusEl.textContent = '';
                }, 2000);
            } else {
                throw new Error(data.detail || 'Subscription failed');
            }
        } catch (err) {
            btn.textContent = 'Try Again';
            btn.style.backgroundColor = '#dc3545';
            if (statusEl) {
                statusEl.textContent = `❌ ${err.message}`;
                statusEl.style.color = '#dc3545';
            }

            setTimeout(() => {
                btn.textContent = 'Subscribe';
                btn.style.backgroundColor = '';
                btn.disabled = false;
            }, 2000);
        }
    });
}


// ─── PARALLAX ORBS ──────────────────────────────────────────────────
function initParallax() {
    const orbs = document.querySelectorAll('.orb');

    document.addEventListener('mousemove', (e) => {
        const x = e.clientX / window.innerWidth - 0.5;
        const y = e.clientY / window.innerHeight - 0.5;

        orbs.forEach((orb, index) => {
            const speed = (index + 1) * 20;
            const xOffset = x * speed;
            const yOffset = y * speed;
            orb.style.transform = `translate(${xOffset}px, ${yOffset}px) scale(${1 + (index * 0.02)})`;
        });
    });
}

