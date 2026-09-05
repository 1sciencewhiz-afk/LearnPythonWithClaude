/* A small dependency-free Python editor: line numbers, smart indenting,
   and syntax highlighting drawn on a layer behind a transparent textarea. */
(function () {
  "use strict";

  var KEYWORDS = ["False","None","True","and","as","assert","async","await","break","class",
    "continue","def","del","elif","else","except","finally","for","from","global","if","import",
    "in","is","lambda","nonlocal","not","or","pass","raise","return","try","while","with","yield"];
  var BUILTINS = ["abs","all","any","bool","dict","enumerate","filter","float","format","input",
    "int","isinstance","len","list","map","max","min","print","range","repr","reversed","round",
    "set","sorted","str","sum","tuple","type","zip"];

  var KEYWORD_SET = new Set(KEYWORDS);
  var BUILTIN_SET = new Set(BUILTINS);

  function escapeHtml(text) {
    return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  /* Hand-rolled tokenizer. Order matters: comments and strings win over
     everything else, so a '#' inside a string is not treated as a comment. */
  function highlight(source) {
    var out = "";
    var i = 0;
    while (i < source.length) {
      var ch = source[i];

      if (ch === "#") {
        var end = source.indexOf("\n", i);
        if (end === -1) end = source.length;
        out += '<span class="tok-com">' + escapeHtml(source.slice(i, end)) + "</span>";
        i = end;
        continue;
      }

      if (ch === '"' || ch === "'") {
        var triple = source.substr(i, 3);
        var quote = (triple === '"""' || triple === "'''") ? triple : ch;
        var j = i + quote.length;
        while (j < source.length) {
          if (source[j] === "\\") { j += 2; continue; }
          if (source.substr(j, quote.length) === quote) { j += quote.length; break; }
          if (quote.length === 1 && source[j] === "\n") break;
          j += 1;
        }
        if (j > source.length) j = source.length;
        out += '<span class="tok-str">' + escapeHtml(source.slice(i, j)) + "</span>";
        i = j;
        continue;
      }

      if (/[0-9]/.test(ch)) {
        var num = /^[0-9_]*\.?[0-9_]*(?:[eE][-+]?[0-9]+)?/.exec(source.slice(i))[0];
        out += '<span class="tok-num">' + escapeHtml(num) + "</span>";
        i += num.length;
        continue;
      }

      if (/[A-Za-z_]/.test(ch)) {
        var word = /^[A-Za-z_][A-Za-z0-9_]*/.exec(source.slice(i))[0];
        var after = source.slice(i + word.length);
        var cls = "";
        if (KEYWORD_SET.has(word)) cls = "tok-kw";
        else if (/^\s*\(/.test(after)) cls = BUILTIN_SET.has(word) ? "tok-fn" : "tok-def";
        out += cls ? '<span class="' + cls + '">' + escapeHtml(word) + "</span>" : escapeHtml(word);
        i += word.length;
        continue;
      }

      out += escapeHtml(ch);
      i += 1;
    }
    return out;
  }

  function CodeEditor(root) {
    this.root = root;
    this.input = root.querySelector(".editor-input");
    this.layer = root.querySelector(".editor-highlight");
    this.gutter = root.querySelector(".editor-gutter");
    this.bind();
    this.render();
  }

  CodeEditor.prototype.bind = function () {
    var self = this;
    this.input.addEventListener("input", function () { self.render(); });
    this.input.addEventListener("scroll", function () { self.syncScroll(); });
    this.input.addEventListener("keydown", function (event) { self.onKeyDown(event); });
  };

  CodeEditor.prototype.value = function () { return this.input.value; };

  CodeEditor.prototype.setValue = function (text) {
    this.input.value = text;
    this.render();
    this.input.focus();
  };

  CodeEditor.prototype.render = function () {
    var text = this.input.value;
    // A trailing newline needs a placeholder or the last line has no height.
    this.layer.innerHTML = highlight(text) + (text.endsWith("\n") ? " " : "");
    var lines = text.split("\n").length;
    var numbers = "";
    for (var n = 1; n <= lines; n++) numbers += n + "\n";
    this.gutter.textContent = numbers;
    this.syncScroll();
  };

  CodeEditor.prototype.syncScroll = function () {
    this.layer.scrollTop = this.input.scrollTop;
    this.layer.scrollLeft = this.input.scrollLeft;
    this.gutter.scrollTop = this.input.scrollTop;
  };

  CodeEditor.prototype.insert = function (text, caretOffset) {
    var start = this.input.selectionStart;
    var end = this.input.selectionEnd;
    var value = this.input.value;
    this.input.value = value.slice(0, start) + text + value.slice(end);
    var caret = start + (caretOffset === undefined ? text.length : caretOffset);
    this.input.selectionStart = this.input.selectionEnd = caret;
    this.render();
  };

  CodeEditor.prototype.onKeyDown = function (event) {
    var input = this.input;
    var start = input.selectionStart;
    var end = input.selectionEnd;
    var value = input.value;

    if (event.key === "Tab") {
      event.preventDefault();
      if (start !== end) {
        this.indentSelection(event.shiftKey);
      } else if (event.shiftKey) {
        var lineStart = value.lastIndexOf("\n", start - 1) + 1;
        if (value.slice(lineStart, lineStart + 4) === "    ") {
          input.value = value.slice(0, lineStart) + value.slice(lineStart + 4);
          input.selectionStart = input.selectionEnd = Math.max(lineStart, start - 4);
          this.render();
        }
      } else {
        this.insert("    ");
      }
      return;
    }

    if (event.key === "Enter") {
      // Keep the current indent, and add one level after a line ending in ':'.
      var head = value.slice(0, start);
      var line = head.slice(head.lastIndexOf("\n") + 1);
      var indent = (/^[ \t]*/.exec(line) || [""])[0];
      if (/:\s*$/.test(line)) indent += "    ";
      event.preventDefault();
      this.insert("\n" + indent);
      return;
    }

    if (event.key === "Backspace" && start === end) {
      // Delete a full four-space indent step in one press.
      var before = value.slice(0, start);
      if (/(^|\n)[ ]+$/.test(before) && before.slice(-4) === "    ") {
        event.preventDefault();
        input.value = value.slice(0, start - 4) + value.slice(start);
        input.selectionStart = input.selectionEnd = start - 4;
        this.render();
      }
    }
  };

  CodeEditor.prototype.indentSelection = function (outdent) {
    var input = this.input;
    var value = input.value;
    var from = value.lastIndexOf("\n", input.selectionStart - 1) + 1;
    var to = input.selectionEnd;
    var block = value.slice(from, to);
    var updated = outdent
      ? block.replace(/^ {1,4}/gm, "")
      : block.replace(/^/gm, "    ");
    input.value = value.slice(0, from) + updated + value.slice(to);
    input.selectionStart = from;
    input.selectionEnd = from + updated.length;
    this.render();
  };

  window.CodeEditor = CodeEditor;
  window.highlightPython = highlight;

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-editor]").forEach(function (root) {
      root.editor = new CodeEditor(root);
    });
  });
})();
