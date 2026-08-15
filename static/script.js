(function () {
  const body = document.body;
  if (!body.classList.contains("room")) return; // only run on the room page

  const CODE = body.dataset.code;
  const NAME = body.dataset.name;
  const SIZE = parseInt(body.dataset.size, 10);
  const IS_HOST = body.dataset.host === "true";

  const boardEl = document.getElementById("board");
  const playerListEl = document.getElementById("playerList");
  const logListEl = document.getElementById("logList");
  const hostControlsEl = document.getElementById("hostControls");
  const noteBanner = document.getElementById("noteBanner");
  const bingoToast = document.getElementById("bingoToast");
  const codeBadge = document.getElementById("codeBadge");

  let playerColors = {}; // name -> color
  let prevMarkedSet = new Set();
  let prevLinesSet = new Set();

  if (IS_HOST) hostControlsEl.hidden = false;

  // ---------- rendering ----------

  function cellMarkup(cell, index) {
    const diff = (cell.difficulty || "").toLowerCase();
    return `
      <button class="cell diff-${diff}" id="cell-${index}" data-index="${index}"
              data-category="${cell.category}" data-difficulty="${cell.difficulty}">
        <span class="cell-tag">${cell.category} · ${cell.difficulty}</span>
        <span class="cell-text">${cell.text}</span>
        <span class="cell-marks"></span>
      </button>`;
  }

  function renderBoardCells(board) {
    boardEl.style.setProperty("--size", SIZE);
    boardEl.innerHTML = board.map(cellMarkup).join("");
  }

  function lineIndices(lineId, size) {
    const [kind, numStr] = lineId.split("-");
    const n = parseInt(numStr, 10);
    const idx = [];
    if (kind === "row") {
      for (let c = 0; c < size; c++) idx.push(n * size + c);
    } else if (kind === "col") {
      for (let r = 0; r < size; r++) idx.push(r * size + n);
    } else if (kind === "diag" && n === 0) {
      for (let i = 0; i < size; i++) idx.push(i * (size + 1));
    } else if (kind === "diag" && n === 1) {
      for (let i = 0; i < size; i++) idx.push((size - 1) + i * (size - 1));
    }
    return idx;
  }

  function applyMarks(marks, lines, opts) {
    opts = opts || {};
    const markedSet = new Set(Object.keys(marks).map((k) => parseInt(k, 10)));
    const coveredSet = new Set();
    lines.forEach((lineId) => lineIndices(lineId, SIZE).forEach((i) => coveredSet.add(i)));

    for (let i = 0; i < SIZE * SIZE; i++) {
      const el = document.getElementById(`cell-${i}`);
      if (!el) continue;
      const names = marks[String(i)] || [];
      el.classList.toggle("marked", names.length > 0);
      el.classList.toggle("in-line", coveredSet.has(i));

      const marksSpan = el.querySelector(".cell-marks");
      if (marksSpan) {
        marksSpan.innerHTML = names
          .map((n) => `<span class="mark-chip" style="background:${playerColors[n] || "#c9a227"}" title="${n}"></span>`)
          .join("");
      }

      if (!opts.skipEffects && markedSet.has(i) && !prevMarkedSet.has(i)) {
        el.classList.remove("flash");
        void el.offsetWidth; // restart animation
        el.classList.add("flash");
        setTimeout(() => el.classList.remove("flash"), 750);
      }
    }

    if (!opts.skipEffects) {
      const newLines = lines.filter((l) => !prevLinesSet.has(l));
      if (newLines.length > 0) showBingoToast();
    }

    prevMarkedSet = markedSet;
    prevLinesSet = new Set(lines);
  }

  function showBingoToast() {
    bingoToast.classList.add("show");
    setTimeout(() => bingoToast.classList.remove("show"), 2200);
  }

  function renderPlayers(players) {
    playerColors = {};
    players.forEach((p) => (playerColors[p.name] = p.color));
    playerListEl.innerHTML = players
      .map(
        (p) => `<li><span class="player-dot" style="background:${p.color}"></span>${p.name}${
          p.name === NAME ? " (you)" : ""
        }</li>`
      )
      .join("");
  }

  function addLog(text) {
    const li = document.createElement("li");
    li.textContent = text;
    logListEl.prepend(li);
    while (logListEl.children.length > 30) logListEl.removeChild(logListEl.lastChild);
  }

  function setNote(text) {
    if (!text) {
      if (noteBanner) noteBanner.remove();
      return;
    }
    if (!noteBanner) {
      const div = document.createElement("div");
      div.className = "banner banner-note";
      div.id = "noteBanner";
      div.textContent = text;
      boardEl.parentElement.prepend(div);
    } else {
      noteBanner.textContent = text;
    }
  }

  // ---------- initial paint (before socket connects) ----------

  try {
    const initial = JSON.parse(document.getElementById("initialState").textContent);
    applyMarks(initial.marks || {}, [], { skipEffects: true });
  } catch (e) {
    /* no-op */
  }

  // ---------- socket wiring ----------

  const socket = io();

  socket.on("connect", () => {
    socket.emit("join", { code: CODE, name: NAME });
  });

  socket.on("state", (data) => {
    renderBoardCells(data.board);
    renderPlayers(data.players);
    setNote(data.note);
    prevMarkedSet = new Set();
    prevLinesSet = new Set();
    applyMarks(data.marks, data.lines, { skipEffects: true });
  });

  socket.on("players_update", (players) => renderPlayers(players));

  socket.on("marks_update", (data) => applyMarks(data.marks, data.lines));

  socket.on("toast", (msg) => addLog(msg));

  socket.on("error_msg", (msg) => addLog(`⚠ ${msg}`));

  socket.on("disconnect", () => addLog("Lost the site of grace… reconnecting."));

  // ---------- interactions ----------

  boardEl.addEventListener("click", (e) => {
    const cell = e.target.closest(".cell");
    if (!cell) return;
    socket.emit("toggle_cell", { code: CODE, index: Number(cell.dataset.index) });
  });

  if (codeBadge) {
    codeBadge.addEventListener("click", () => {
      if (navigator.clipboard) {
        navigator.clipboard.writeText(CODE).catch(() => {});
      }
      const valueEl = codeBadge.querySelector(".code-value");
      const original = valueEl.textContent;
      valueEl.textContent = "Copied!";
      setTimeout(() => (valueEl.textContent = original), 900);
    });
  }

  if (IS_HOST) {
    document.getElementById("rerollBtn").addEventListener("click", () => {
      if (confirm("Reroll the board? This clears all current marks for everyone.")) {
        socket.emit("reroll", { code: CODE });
      }
    });
    document.getElementById("resetBtn").addEventListener("click", () => {
      if (confirm("Reset all marks? The board stays the same.")) {
        socket.emit("reset_marks", { code: CODE });
      }
    });
  }
})();
