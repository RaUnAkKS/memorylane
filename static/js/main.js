function fetchNotificationCount() {
  fetch("/api/notifications/count/")
    .then(res => res.json())
    .then(data => {
      const el = document.getElementById("notif-count");
      if (el) {
        el.textContent = data.count;
        el.style.display = data.count > 0 ? "inline-block" : "none";
      }
    })
    .catch(() => {});
}

// Run immediately
fetchNotificationCount();

// Poll every 5 seconds
setInterval(fetchNotificationCount, 5000);

document.addEventListener("DOMContentLoaded", () => {
  const checkbox = document.getElementById("customThemeCheck");
  const input = document.getElementById("customThemeInput");

  if (checkbox && input) {
    checkbox.addEventListener("change", () => {
      input.style.display = checkbox.checked ? "block" : "none";
    });
  }
});

function toggleUser(card, selectId) {
  const userId = card.dataset.value;
  const select = document.getElementById(selectId);

  if (!select) return;

  const option = Array.from(select.options)
    .find(opt => opt.value === userId);

  if (!option) return;

  option.selected = !option.selected;
  card.classList.toggle("selected", option.selected);
}

function filterUserCards(input, containerId) {
  const filter = input.value.toLowerCase();
  const container = document.getElementById(containerId);

  if (!container) return;

  Array.from(container.children).forEach(card => {
    card.style.display =
      card.textContent.toLowerCase().includes(filter)
        ? "inline-flex"
        : "none";
  });
}
