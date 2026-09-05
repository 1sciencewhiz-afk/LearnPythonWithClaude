/* Wires the lesson player to the run / check endpoints. */
(function () {
  "use strict";

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  function escapeHtml(text) {
    return String(text).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  ready(function () {
    var panel = document.querySelector("[data-lesson]");
    if (!panel) return;

    var slug = panel.dataset.lesson;
    var csrf = panel.dataset.csrf;
    var runUrl = panel.dataset.runUrl;
    var checkUrl = panel.dataset.checkUrl;
    var solutionUrl = panel.dataset.solutionUrl;
    var tracksUrl = panel.dataset.tracksUrl;

    var shell = document.querySelector("[data-editor]");
    var editor = shell.editor || new window.CodeEditor(shell);
    var starter = panel.dataset.starter || "";

    var runBtn = document.getElementById("run-btn");
    var checkBtn = document.getElementById("check-btn");
    var resetBtn = document.getElementById("reset-btn");
    var solutionBtn = document.getElementById("solution-btn");
    var stdinBox = document.getElementById("stdin");
    var consoleBox = document.getElementById("console");
    var resultsBox = document.getElementById("results");

    function setBusy(busy, label) {
      [runBtn, checkBtn].forEach(function (btn) { if (btn) btn.disabled = busy; });
      if (busy) consoleBox.textContent = label;
    }

    function post(url) {
      return fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
        body: JSON.stringify({ code: editor.value(), stdin: stdinBox ? stdinBox.value : "" })
      }).then(function (response) {
        return response.json().then(function (data) { return { status: response.status, data: data }; });
      });
    }

    function renderError(error) {
      if (!error) return "";
      var where = error.line ? " (line " + error.line + ")" : "";
      return (
        '<div class="error-box">' +
        '<div class="error-title">' + escapeHtml(error.type) + where + "</div>" +
        "<div>" + escapeHtml(error.message) + "</div>" +
        (error.hint ? '<div class="error-hint">' + escapeHtml(error.hint) + "</div>" : "") +
        "</div>"
      );
    }

    function renderChecks(results) {
      if (!results || !results.length) return "";
      var items = results.map(function (result) {
        var detail = "";
        if (!result.passed) {
          if (result.error) {
            detail = '<div class="result-detail">' + escapeHtml(result.error.message) + "</div>";
          } else if (result.call) {
            detail = '<div class="result-detail">' + escapeHtml(result.call) +
              " gave " + escapeHtml(result.got) + ", expected " + escapeHtml(result.expected) + "</div>";
          } else if (result.got !== null && result.got !== undefined) {
            // An output check: show both sides so the difference is obvious.
            var want = Array.isArray(result.expected) ? result.expected.join("\n") : result.expected;
            var wanted = result.match === "contains" ? "Your output should contain: "
              : result.match === "regex" ? "Your output should match: "
              : "Expected output: ";
            detail = '<div class="result-detail">' + escapeHtml(wanted) +
              escapeHtml(want) + "</div>" +
              '<div class="result-detail">You printed: ' +
              escapeHtml(result.got || "(nothing)") + "</div>";
          } else if (result.expected) {
            detail = '<div class="result-detail">Needed: ' + escapeHtml(result.expected) + "</div>";
          }
        }
        return (
          '<li class="result ' + (result.passed ? "pass" : "fail") + '">' +
          '<span class="mark" aria-hidden="true">' + (result.passed ? "✓" : "✗") + "</span>" +
          "<div><strong>" + escapeHtml(result.label) + "</strong>" + detail + "</div></li>"
        );
      });
      return '<ul class="result-list">' + items.join("") + "</ul>";
    }

    function renderSuccess(data) {
      var parts = ["<h3>Lesson complete!</h3>"];
      if (data.first_time && data.xp_gained) {
        parts.push("<p>You earned <strong>" + data.xp_gained + " XP</strong>. " +
          "You are level " + data.level + " with a " + data.streak + "-day streak.</p>");
      } else {
        parts.push("<p>Passed again - your progress was already saved.</p>");
      }
      (data.new_badges || []).forEach(function (badge) {
        parts.push('<div class="badge-pop"><span aria-hidden="true">' + badge.emoji + "</span>" +
          "<span>New badge: <strong>" + escapeHtml(badge.name) + "</strong> - " +
          escapeHtml(badge.description) + "</span></div>");
      });
      if (data.next_url) {
        parts.push('<p class="mb-0"><a class="btn" href="' + data.next_url + '">Next: ' +
          escapeHtml(data.next_title) + "</a></p>");
      } else {
        parts.push('<p class="mb-0">That is the last lesson in this track. ' +
          '<a href="' + tracksUrl + '">Choose another track</a>.</p>');
      }
      return '<div class="celebrate">' + parts.join("") + "</div>";
    }

    function showOutput(data) {
      consoleBox.textContent = (data.stdout || "") + (data.stderr || "");
    }

    if (runBtn) {
      runBtn.addEventListener("click", function () {
        setBusy(true, "Running your code...");
        post(runUrl).then(function (payload) {
          setBusy(false);
          showOutput(payload.data);
          resultsBox.innerHTML = renderError(payload.data.error);
        }).catch(function () {
          setBusy(false);
          consoleBox.textContent = "Could not reach the server. Check your connection and try again.";
        });
      });
    }

    if (checkBtn) {
      checkBtn.addEventListener("click", function () {
        setBusy(true, "Checking your answer...");
        post(checkUrl).then(function (payload) {
          setBusy(false);
          var data = payload.data;
          showOutput(data);
          var html = renderError(data.error) + renderChecks(data.results);
          if (data.passed) html += renderSuccess(data);
          resultsBox.innerHTML = html;
          if (data.show_solution && solutionBtn) solutionBtn.hidden = false;
          if (data.passed) {
            resultsBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
          }
        }).catch(function () {
          setBusy(false);
          consoleBox.textContent = "Could not reach the server. Check your connection and try again.";
        });
      });
    }

    if (resetBtn) {
      resetBtn.addEventListener("click", function () {
        if (window.confirm("Replace your code with the starter code?")) {
          editor.setValue(starter);
          resultsBox.innerHTML = "";
          consoleBox.textContent = "";
        }
      });
    }

    if (solutionBtn) {
      solutionBtn.addEventListener("click", function () {
        fetch(solutionUrl).then(function (r) { return r.json(); }).then(function (data) {
          if (!data.available) {
            resultsBox.innerHTML = '<div class="error-box"><div class="error-title">Not yet</div>' +
              "<div>Try " + data.attempts_needed + " more time(s) first - you are closer than you think.</div></div>";
            return;
          }
          var box = document.getElementById("solution-box");
          box.innerHTML = "<h3>One way to solve it</h3><pre><code>" +
            window.highlightPython(data.solution) + "</code></pre>" +
            '<p class="faint">Compare it with yours - a different working answer is still a right answer.</p>';
          box.hidden = false;
          solutionBtn.hidden = true;
        });
      });
    }

    // Ctrl/Cmd+Enter checks the answer, the way most editors run code.
    document.addEventListener("keydown", function (event) {
      if ((event.ctrlKey || event.metaKey) && event.key === "Enter" && checkBtn) {
        event.preventDefault();
        checkBtn.click();
      }
    });
  });
})();
