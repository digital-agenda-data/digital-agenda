
function getCookie(name) {
  name = name.toLowerCase()
  for (const cookie of document.cookie.split(";")) {
    const [key, value] = cookie.split("=");
    if (key.trim().toLowerCase() === name) {
      return value
    }
  }
}


/**
 * Detect the user timezone and send it to the backend.
 */
function setTimezone() {
  const csrfToken = getCookie("csrftoken");
  const currentTimezone = getCookie("X-Django-Timezone")
  const detectedTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

  if (currentTimezone && JSON.parse(currentTimezone) === detectedTimezone) {
    // Timezone is already set, nothing to do.
    return;
  }

  fetch("/api/v1/set-timezone/", {
    method: "POST",
    credentials: "include",
    body: JSON.stringify({
      timezone: detectedTimezone,
    }),
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    }

  });
}

try {
  setTimezone();
} catch (e) {
  console.warn("Unable to set timezone", e)
}