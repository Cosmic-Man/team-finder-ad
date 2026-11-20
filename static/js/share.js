document.addEventListener("click", function (event) {
  const shareButton = event.target.closest(".share-button");
  if (!shareButton) return;

  event.preventDefault();

  const shareUrl = shareButton.dataset.url
    ? window.location.origin + shareButton.dataset.url
    : window.location.href;

  navigator.clipboard
    .writeText(shareUrl)
    .then(() => {
      if (window.toast) {
        window.toast(`Ссылка скопирована: ${shareUrl}`, { type: "info" });
      } else {
        alert(`Ссылка скопирована: ${shareUrl}`);
      }
    })
    .catch((error) => {
      console.error("Ошибка копирования:", error);
      fallbackCopyTextToClipboard(shareUrl);
    });
});

function fallbackCopyTextToClipboard(value) {
  try {
    const temporaryInput = document.createElement("textarea");
    temporaryInput.value = value;
    temporaryInput.setAttribute("readonly", "");
    temporaryInput.style.position = "fixed";
    temporaryInput.style.top = "-1000px";
    document.body.appendChild(temporaryInput);
    temporaryInput.focus();
    temporaryInput.select();
    const copySucceeded = document.execCommand("copy");
    document.body.removeChild(temporaryInput);

    if (!copySucceeded) throw new Error("document.execCommand copy failed");
    if (window.toast) {
      window.toast(`Ссылка скопирована: ${value}`, { type: "info" });
    } else {
      alert(`Ссылка скопирована: ${value}`);
    }
  } catch (error) {
    console.error("Ошибка копирования (fallback):", error);
    window.prompt("Скопируйте ссылку:", value);
  }
}
