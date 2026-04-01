document.addEventListener("DOMContentLoaded", function () {
    console.log("timeout.js loaded");

    // Retrieve session banner elements from DOM
    const banner = document.getElementById("session-banner-shell");
    if (!banner) {
        console.log("No session timeout banner found.");
        return;
    }

    let remaining = parseInt(banner.dataset.secondsRemaining, 10);
    const extendUrl = banner.dataset.extendUrl;
    const expireUrl = banner.dataset.expireUrl;

    const warningThreshold = 30; // Adjustable, this is in seconds

    const titleEl = document.getElementById("session-timeout-title");
    const textEl = document.getElementById("session-timeout-text");
    const countdownEl = document.getElementById("session-timeout-countdown");
    const extendBtn = document.getElementById("extend-session-btn");
    const reloginBtn = document.getElementById("relogin-btn");

    let sessionExpiredHandled = false;

    console.log("Initial remaining seconds:", remaining);

    // Time formatting for display
    function formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, "0")}`;
    }

    // Retrieve a cookie by name; used for getting CSRF token for POST requests
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Handle backend request
    async function postSessionAction(url) {
        const csrfToken = getCookie("csrftoken");

        const response = await fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "X-Requested-With": "XMLHttpRequest"
            },
            credentials: "same-origin"
        });

        return response;
    }

    // Render banner based on the state
    function renderBanner(state) {

        const isHidden = state === "hidden";
        const isExpired = state === "expired";
        const isWarning = state === "warning";

        banner.classList.toggle("is-visible", !isHidden);
        banner.classList.toggle("alert-warning", isWarning || isHidden);
        banner.classList.toggle("alert-danger", isExpired);

        extendBtn.classList.toggle("d-none", isExpired);
        extendBtn.disabled = false;

        reloginBtn.classList.toggle("d-none", !isExpired);

        if (isHidden) return;
        
        if (isWarning) {
            titleEl.textContent = "Warning:";
            textEl.textContent = "Your CampusBridge session will expire in";
            countdownEl.textContent = formatTime(remaining);
        } else { // expired
            titleEl.textContent = "Your session has expired.";
            textEl.textContent = "Please log in again.";
            countdownEl.textContent = "";
        }
    }

    // Decides which banner state should be shown, rendered automatically
    function updateBannerUI() {
        console.log("updateBannerUI remaining =", remaining);
        
        if (remaining <= 0) {
            return renderBanner("expired");
        } else if (remaining <= warningThreshold) {
            return renderBanner("warning");
        } else {
            return renderBanner("hidden");
        }
    }

    // Expires a session
    async function expireSession() {

        if (sessionExpiredHandled) return;
        sessionExpiredHandled = true;

        try {
            await postSessionAction(expireUrl);
            console.log("Session successfully expired on backend.");
        } catch (error) {
            console.error("Session expiration failed.");
        }
    }

    updateBannerUI();

    // Set countdown timer
    const timer = setInterval(() => {

        remaining -= 1;
        console.log("tick:", remaining);
        updateBannerUI();

        if (remaining <= 0) {
            clearInterval(timer);
            expireSession();
        }
    }, 1000);

    // Extend session upon request
    extendBtn.addEventListener("click", async function () {

        try {
            const response = await postSessionAction(extendUrl);
            const data = await response.json();

            remaining = parseInt(data.remaining_seconds, 10);
            sessionExpiredHandled = false;

            console.log("Session extended:", remaining);
            updateBannerUI();
        } catch (error) {
            console.error("Session extension failed.");
        }
    });

    window.addEventListener("pageshow", function (event) {
        if (event.persisted) {
            window.location.reload();
        }
    });
});