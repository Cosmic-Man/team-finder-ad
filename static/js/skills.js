(function () {
  document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("skills-container");
    if (!container) return;

    const projectId = container.dataset.projectId;
    const userId = container.dataset.userId;

    let skillsUrl, addUrl, removeUrl;
    if (userId) {
      skillsUrl = `/users/skills/`;
      addUrl = `/users/${userId}/skills/add/`;
      removeUrl = (skillId) => `/users/${userId}/skills/${skillId}/remove/`;
    } else {
      skillsUrl = `/projects/skills/`;
      addUrl = `/projects/${projectId}/skills/add/`;
      removeUrl = (skillId) => `/projects/${projectId}/skills/${skillId}/remove/`;
    }

    const addButton = document.getElementById("add-skill-btn");
    const inputWrapper = document.getElementById("skill-input-wrapper");
    const input = document.getElementById("skill-input");
    const suggestions = document.getElementById("skill-suggestions");

    if (!addButton || !inputWrapper || !input || !suggestions) return;

    addButton.addEventListener("click", () => {
      addButton.classList.add("hidden");
      inputWrapper.classList.remove("hidden");
      input.value = "";
      suggestions.innerHTML = "";
      suggestions.classList.add("hidden");
      input.focus();
    });

    let searchTimeout = null;
    input.addEventListener("input", () => {
      const searchQuery = input.value.trim();
      clearTimeout(searchTimeout);
      if (!searchQuery) {
        suggestions.classList.add("hidden");
        suggestions.innerHTML = "";
        return;
      }
      searchTimeout = setTimeout(async () => {
        const response = await fetch(
          `${skillsUrl}?q=${encodeURIComponent(searchQuery)}`
        );
        if (!response.ok) return;
        const matchingSkills = await response.json();

        suggestions.innerHTML = "";
        matchingSkills.forEach((skill) => {
          const suggestion = document.createElement("li");
          suggestion.textContent = skill.name;
          suggestion.dataset.id = skill.id;
          suggestion.className = "suggestion-item";
          suggestions.appendChild(suggestion);
        });

        const hasExactMatch = matchingSkills.some(
          (skill) => skill.name.toLowerCase() === searchQuery.toLowerCase()
        );
        if (!hasExactMatch) {
          const createSuggestion = document.createElement("li");
          createSuggestion.textContent = `Создать «${searchQuery}»`;
          createSuggestion.dataset.name = searchQuery;
          createSuggestion.className = "create-new";
          suggestions.appendChild(createSuggestion);
        }

        suggestions.classList.remove("hidden");
      }, 200);
    });

    suggestions.addEventListener("mousedown", async (event) => {
      const suggestion = event.target.closest("li");
      if (!suggestion) return;

      if (suggestion.classList.contains("create-new")) {
        await addSkillByName(suggestion.dataset.name);
      } else if (suggestion.dataset.id) {
        await addSkillById(suggestion.dataset.id);
      }
      hideInput();
    });

    input.addEventListener("keydown", async (event) => {
      if (event.key === "Enter") {
        event.preventDefault();
        const searchQuery = input.value.trim();
        if (!searchQuery) return;

        const firstSuggestion = suggestions.querySelector("li");
        if (firstSuggestion && firstSuggestion.dataset.id) {
          await addSkillById(firstSuggestion.dataset.id);
        } else {
          await addSkillByName(searchQuery);
        }
        hideInput();
      }
      if (event.key === "Escape") {
        hideInput();
      }
    });

    input.addEventListener("blur", () => setTimeout(hideInput, 120));

    function hideInput() {
      inputWrapper.classList.add("hidden");
      suggestions.classList.add("hidden");
      addButton.classList.remove("hidden");
    }

    container.addEventListener("click", async (event) => {
      if (event.target.classList.contains("remove-skill-btn")) {
        const chip = event.target.closest(".skill-chip");
        const skillId = chip.dataset.id;
        const response = await fetch(removeUrl(skillId), {
          method: "POST",
          headers: { "X-CSRFToken": window.getCookie("csrftoken") },
        });
        if (response.ok) {
          chip.remove();
        }
      }
    });

    async function addSkillById(skillId) {
      const response = await fetch(addUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": window.getCookie("csrftoken"),
        },
        body: JSON.stringify({ skill_id: skillId }),
      });
      if (response.ok) {
        const skill = await response.json();
        appendChip(skill.id, skill.name);
      }
    }

    async function addSkillByName(skillName) {
      const response = await fetch(addUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": window.getCookie("csrftoken"),
        },
        body: JSON.stringify({ name: skillName }),
      });
      if (response.ok) {
        const skill = await response.json();
        appendChip(skill.id, skill.name);
      }
    }

    function appendChip(skillId, skillName) {
      if (container.querySelector(`.skill-chip[data-id="${skillId}"]`)) return;

      const chip = document.createElement("span");
      chip.className = "skill-chip";
      chip.dataset.id = skillId;
      chip.append(document.createTextNode(`${skillName} `));

      const removeButton = document.createElement("button");
      removeButton.type = "button";
      removeButton.className = "remove-skill-btn";
      removeButton.setAttribute("aria-label", "Удалить");
      removeButton.title = "Удалить";
      removeButton.textContent = "×";
      chip.appendChild(removeButton);

      container.insertBefore(chip, addButton);

      const empty = container.querySelector(".skill-empty");
      if (empty) empty.remove();
    }

  });
})();
