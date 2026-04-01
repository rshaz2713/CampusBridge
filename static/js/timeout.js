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

    // Banner state functions. Hidden state
    function hideBannerState() {
        banner.classList.remove("is-visible", "alert-danger");
        banner.classList.add("alert-warning");

        extendBtn.classList.remove("d-none");
        extendBtn.disabled = false;
        reloginBtn.classList.add("d-none");
    }

    // Warning state
    function showWarningState() {
        banner.classList.add("is-visible");
        banner.classList.remove("alert-danger");
        banner.classList.add("alert-warning");

        titleEl.textContent = "Warning:";
        textEl.textContent = "Your CampusBridge session will expire in";
        countdownEl.textContent = formatTime(remaining);

        extendBtn.classList.remove("d-none");
        extendBtn.disabled = false;
        reloginBtn.classList.add("d-none");
    }

    // Expired state (re-login required)
    function showExpiredState() {
        banner.classList.add("is-visible");
        banner.classList.remove("alert-warning");
        banner.classList.add("alert-danger");

        titleEl.textContent = "Your session has expired.";
        textEl.textContent = "Please log in again.";
        countdownEl.textContent = "";

        extendBtn.classList.add("d-none");
        reloginBtn.classList.remove("d-none");
    }

    // Decides which UI state should be shown, rendered automatically
    function updateUI() {
        console.log("updateUI remaining =", remaining);

        if (remaining <= 0) {
            showExpiredState();
        } else if (remaining <= warningThreshold) {
            showWarningState();
        } else {
            hideBannerState();
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

    updateUI();

    // Set countdown timer
    const timer = setInterval(() => {

        remaining -= 1;
        console.log("tick:", remaining);
        updateUI();

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
            updateUI();
        } catch (error) {
            console.error("Session extension failed.");
        }
    });
});