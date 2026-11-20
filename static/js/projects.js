(function () {
  document.addEventListener("DOMContentLoaded", function () {
    const completeButton = document.getElementById("complete-project-btn");
    if (completeButton) {
      completeButton.addEventListener("click", function (event) {
        event.preventDefault();
        const projectId = completeButton.dataset.id;
        if (!projectId) return;

        fetch(`/projects/${projectId}/complete/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": window.getCookie
              ? window.getCookie("csrftoken")
              : "",
            "Content-Type": "application/json",
          },
          body: JSON.stringify({}),
        })
          .then((response) => response.json())
          .then((result) => {
            if (result.status === "ok") {
              const projectStatus = document.querySelector(
                ".project-status-black"
              );
              if (projectStatus) projectStatus.textContent = "Закрыт";
              completeButton.remove();
              if (window.toast) {
                window.toast("Проект завершён", { type: "info" });
              }
            } else if (window.toast) {
              window.toast("Ошибка при завершении проекта", { type: "error" });
            } else {
              alert("Ошибка при завершении проекта");
            }
          })
          .catch((error) => {
            console.error("Ошибка запроса:", error);
            if (window.toast) window.toast("Ошибка сети", { type: "error" });
          });
      });
    }

    const participateButton = document.getElementById("participate-btn");
    const participantsList = document.getElementById("participants-list");
    const participantsCount = document.getElementById("participants-count");
    if (!participateButton || !participantsList || !participantsCount) return;

    const userId = participateButton.dataset.userId || null;
    const projectId = participateButton.dataset.project;
    const userName = participateButton.dataset.userName || "";
    const userAvatar = participateButton.dataset.userAvatar || "";

    participateButton.addEventListener("click", function (event) {
      event.preventDefault();
      if (!projectId) return;

      fetch(`/projects/${projectId}/toggle-participate/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": window.getCookie
            ? window.getCookie("csrftoken")
            : "",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({}),
      })
        .then((response) => response.json())
        .then((result) => {
          if (result.status !== "ok") {
            if (window.toast) {
              window.toast("Ошибка при изменении участия", { type: "error" });
            } else {
              alert("Ошибка при изменении участия");
            }
            return;
          }

          if (result.participant) {
            participateButton.textContent = "Отказаться от участия";

            const emptyState = document.getElementById("no-participants");
            if (emptyState) emptyState.remove();

            const participantLink = document.createElement("a");
            participantLink.href = `/users/${userId}`;
            participantLink.id = `participant-${userId}`;
            participantLink.innerHTML = `
              <div class="participant-item">
                <img src="${userAvatar}" alt="Аватар" class="participant-avatar">
                <div class="participant-info">
                  <span class="participant-name">${userName}</span>
                  <span class="participant-role">Участник</span>
                </div>
              </div>
            `;
            participantsList.appendChild(participantLink);
            participantsCount.textContent =
              Number.parseInt(participantsCount.textContent, 10) + 1;
            return;
          }

          participateButton.textContent = "Участвовать";
          const participantElement = document.getElementById(
            `participant-${userId}`
          );
          if (participantElement) participantElement.remove();

          const updatedCount =
            Number.parseInt(participantsCount.textContent, 10) - 1;
          participantsCount.textContent = updatedCount;

          if (updatedCount === 0) {
            const emptyState = document.createElement("p");
            emptyState.id = "no-participants";
            emptyState.textContent = "Пока нет участников";
            participantsList.appendChild(emptyState);
          }
        })
        .catch((error) => {
          console.error("Ошибка запроса:", error);
          if (window.toast) window.toast("Ошибка сети", { type: "error" });
        });
    });
  });
})();
