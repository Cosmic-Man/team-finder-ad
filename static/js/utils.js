(function () {
  if (!window.getCookie) {
    window.getCookie = function (name) {
      const cookiePrefix = `${name}=`;
      const cookie = document.cookie
        .split(";")
        .map((part) => part.trim())
        .find((part) => part.startsWith(cookiePrefix));

      return cookie
        ? decodeURIComponent(cookie.slice(cookiePrefix.length))
        : null;
    };
  }

  if (!window.toast) {
    function createToastContainer() {
      const existingContainer = document.getElementById("tf-toast-container");
      if (existingContainer) return existingContainer;

      const container = document.createElement("div");
      container.id = "tf-toast-container";
      Object.assign(container.style, {
        position: "fixed",
        left: "50%",
        top: "50%",
        transform: "translate(-50%, -50%)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "8px",
        zIndex: "2147483647",
      });
      document.body.appendChild(container);
      return container;
    }

    window.toast = function (message, options = {}) {
      const { type = "info", duration = 2200 } = options;
      const container = createToastContainer();
      const toastElement = document.createElement("div");

      toastElement.textContent = message;
      Object.assign(toastElement.style, {
        maxWidth: "90vw",
        background:
          type === "error"
            ? "rgba(220, 38, 38, 0.95)"
            : "rgba(17, 17, 17, 0.92)",
        color: "#fff",
        padding: "12px 16px",
        borderRadius: "8px",
        boxShadow: "0 6px 20px rgba(0, 0, 0, 0.25)",
        fontSize: "14px",
        lineHeight: "1.35",
        wordBreak: "break-all",
        textAlign: "center",
        opacity: "0",
        transition: "opacity 180ms ease",
      });

      container.appendChild(toastElement);
      requestAnimationFrame(() => {
        toastElement.style.opacity = "1";
      });

      setTimeout(() => {
        toastElement.style.opacity = "0";
        setTimeout(() => toastElement.remove(), 200);
      }, Math.max(1200, duration));
    };
  }
})();
