document.addEventListener("DOMContentLoaded", function () {
    console.log("timeout.js loaded");

    // Get document elements
    const banner = document.getElementById("session-timeout-banner");
    if (!banner) {
        console.log("No session timeout banner found.");
        return;
    }

    let remaining = parseInt(banner.dataset.secondsRemaining, 10);
    const extendUrl = banner.dataset.extendUrl;
    const warningThreshold = 20; // Adjustable, this is in seconds

    const titleEl = document.getElementById("session-timeout-title");
    const textEl = document.getElementById("session-timeout-text");
    const countdownEl = document.getElementById("session-timeout-countdown");
    const extendBtn = document.getElementById("extend-session-btn");
    const reloginBtn = document.getElementById("relogin-btn");

    console.log("Initial remaining seconds:", remaining);

    // Get CSRF cookie
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

    function formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, "0")}`;
    }

    // Hide banner
    function hideBannerState() {
        banner.classList.add("d-none");
    }

    // Warning for session about to expire
    function showWarningState() {
        banner.classList.remove("d-none", "alert-danger");
        banner.classList.add("alert-warning");

        titleEl.textContent = "Warning:";
        textEl.textContent = "Your CampusBridge session will expire in";
        countdownEl.textContent = formatTime(remaining);

        extendBtn.classList.remove("d-none");
        extendBtn.disabled = false;
        reloginBtn.classList.add("d-none");
    }

    // Session expired
    function showExpiredState() {
        banner.classList.remove("d-none", "alert-warning");
        banner.classList.add("alert-danger");

        titleEl.textContent = "Your session has expired.";
        textEl.textContent = "Please log in again.";
        countdownEl.textContent = "";

        extendBtn.classList.add("d-none");
        reloginBtn.classList.remove("d-none");
    }

    // Render UI based on time left
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

    updateUI();

    // Timer logic for countdown
    const timer = setInterval(() => {
        if (remaining <= 0) {
            clearInterval(timer);
            showExpiredState();
            return;
        }

        remaining -= 1;
        console.log("tick:", remaining);
        updateUI();

        if (remaining <= 0) {
            clearInterval(timer);
            showExpiredState();
        }
    }, 1000);

    // Resets timer via POST request to Django backedn
    extendBtn.addEventListener("click", async function () {
        try {
            const csrfToken = getCookie("csrftoken");

            const response = await fetch(extendUrl, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "X-Requested-With": "XMLHttpRequest"
                },
                credentials: "same-origin"
            });

            if (!response.ok) {
                throw new Error("Failed to extend session.");
            }

            const data = await response.json();
            remaining = parseInt(data.remaining_seconds, 10);
            console.log("session extended:", remaining);
            updateUI();
        } catch (error) {
            console.error("Session extension failed:", error);
        }
    });
});