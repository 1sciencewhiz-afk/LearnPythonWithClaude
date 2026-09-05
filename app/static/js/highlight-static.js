/* Colours the read-only example blocks with the same tokenizer as the editor. */
document.addEventListener("DOMContentLoaded", function () {
  if (!window.highlightPython) return;
  document.querySelectorAll("pre > code").forEach(function (block) {
    if (block.dataset.highlighted) return;
    block.innerHTML = window.highlightPython(block.textContent);
    block.dataset.highlighted = "1";
  });
});
