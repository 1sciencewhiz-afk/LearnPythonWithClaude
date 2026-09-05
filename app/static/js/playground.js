/* The free-play scratchpad: run anything, no grading. */
(function () {
  "use strict";
  document.addEventListener("DOMContentLoaded", function () {
    var panel = document.querySelector("[data-playground]");
    if (!panel) return;

    var shell = document.querySelector("[data-editor]");
    var editor = shell.editor || new window.CodeEditor(shell);
    var consoleBox = document.getElementById("console");
    var runBtn = document.getElementById("run-btn");
    var stdinBox = document.getElementById("stdin");

    runBtn.addEventListener("click", function () {
      runBtn.disabled = true;
      consoleBox.textContent = "Running...";
      fetch(panel.dataset.runUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": panel.dataset.csrf },
        body: JSON.stringify({ code: editor.value(), stdin: stdinBox.value })
      })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          runBtn.disabled = false;
          var text = (data.stdout || "") + (data.stderr || "");
          if (data.error) {
            text += (text ? "\n" : "") + data.error.message +
              (data.error.hint ? "\n\n" + data.error.hint : "");
          }
          consoleBox.textContent = text || "(your program printed nothing)";
        })
        .catch(function () {
          runBtn.disabled = false;
          consoleBox.textContent = "Could not reach the server.";
        });
    });

    document.addEventListener("keydown", function (event) {
      if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
        event.preventDefault();
        runBtn.click();
      }
    });
  });
})();
