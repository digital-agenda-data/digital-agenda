/**
 * Check if two arrays are equal
 *
 * @param a1 {Array}
 * @param a2 {Array}
 * @return {Boolean}
 */
export function arrayEquals(a1, a2) {
  if (a1.length !== a2.length) return false;
  for (let i = 0; i < a1.length; i++) {
    if (a1[i] !== a2[i]) return false;
  }
  return true;
}

/**
 * Scroll to the hash location in the URL
 */
export function scrollToHash() {
  const el = document.querySelector(window.location.hash);
  if (el) {
    el.scrollIntoView({
      behavior: "smooth",
    });
  }
}
