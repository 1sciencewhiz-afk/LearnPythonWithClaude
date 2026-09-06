/* Wires the retractable AI tutor sidebar to the /api/tutor endpoint.
   Messages are rendered with textContent only - never innerHTML - so a
   reply can never inject markup, regardless of what the model sends back. */
(function () {
  "use strict";

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    var sidebar = document.getElementById("tutor-sidebar");
    var toggle = document.getElementById("tutor-toggle");
    if (!sidebar || !toggle) return;

    var closeBtn = document.getElementById("tutor-close");
    var backdrop = document.getElementById("tutor-backdrop");
    var messagesBox = document.getElementById("tutor-messages");
    var form = document.getElementById("tutor-form");
    var input = document.getElementById("tutor-input");
    var sendBtn = document.getElementById("tutor-send");

    var tutorUrl = sidebar.dataset.tutorUrl;
    var csrf = sidebar.dataset.csrf;
    var enabled = sidebar.dataset.enabled === "true";
    var history = [];
    var greeted = false;

    function setOpen(open) {
      sidebar.classList.toggle("is-open", open);
      sidebar.setAttribute("aria-hidden", open ? "false" : "true");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      if (backdrop) backdrop.hidden = !open;
      if (open) {
        if (!greeted) {
          greeted = true;
          addMessage("assistant", enabled
            ? "Hi! I can see your code and the last thing you ran. Tell me what you are stuck on and I will help you think it through - I will not just give you the answer."
            : "The AI tutor is not turned on for this server yet - ask whoever runs it to add a Gemini API key.");
        }
        if (input) input.focus();
      }
    }

    function addMessage(role, text) {
      var bubble = document.createElement("div");
      bubble.className = "tutor-msg tutor-msg-" + role;
      bubble.textContent = text;
      messagesBox.appendChild(bubble);
      messagesBox.scrollTop = messagesBox.scrollHeight;
      return bubble;
    }

    toggle.addEventListener("click", function () {
      setOpen(!sidebar.classList.contains("is-open"));
    });
    if (closeBtn) closeBtn.addEventListener("click", function () { setOpen(false); });
    if (backdrop) backdrop.addEventListener("click", function () { setOpen(false); });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && sidebar.classList.contains("is-open")) setOpen(false);
    });

    if (input) {
      input.addEventListener("keydown", function (event) {
        if (event.key === "Enter" && !event.shiftKey) {
          event.preventDefault();
          if (form.requestSubmit) form.requestSubmit();
          else form.dispatchEvent(new Event("submit", { cancelable: true }));
        }
      });
    }

    if (form) {
      form.addEventListener("submit", function (event) {
        event.preventDefault();
        if (!enabled || !input) return;
        var message = (input.value || "").trim();
        if (!message) return;

        addMessage("user", message);
        history.push({ role: "user", text: message });
        input.value = "";
        input.disabled = true;
        sendBtn.disabled = true;
        var typing = addMessage("assistant", "Thinking...");
        typing.classList.add("tutor-typing");

        var state = window.LessonState || {};
        fetch(tutorUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
          body: JSON.stringify({
            message: message,
            code: typeof state.getCode === "function" ? state.getCode() : "",
            last_result: state.lastResult || {},
            history: history.slice(-6)
          })
        }).then(function (response) {
          return response.json().then(function (data) { return { status: response.status, data: data }; });
        }).then(function (payload) {
          typing.remove();
          input.disabled = false;
          sendBtn.disabled = false;
          var data = payload.data || {};
          if (data.ok) {
            addMessage("assistant", data.reply);
            history.push({ role: "assistant", text: data.reply });
          } else {
            var message = (data.error && data.error.message) || data.error || "Something went wrong - try again.";
            addMessage("assistant", message);
          }
        }).catch(function () {
          typing.remove();
          input.disabled = false;
          sendBtn.disabled = false;
          addMessage("assistant", "Could not reach the server. Check your connection and try again.");
        });
      });
    }
  });
})();
