// static/js/script.js
document.addEventListener("DOMContentLoaded", () => {
  const navItems = document.querySelectorAll(".nav-item");
  const sections = document.querySelectorAll(".section");
  const pageTitle = document.getElementById("pageTitle");

  // Elements for upload & history
  const uploadForm = document.getElementById("uploadForm");
  const fileInput = document.getElementById("pdfFile");
  const responseBox = document.getElementById("response");
  const downloadBtn = document.getElementById("download");
  const historySection = document.getElementById("history");
  const settingsSection = document.getElementById("settings");

  // Helper: show a response
  function showResponse(html, isError = false) {
    responseBox.innerHTML = html;
    responseBox.classList.add("show");
    responseBox.style.borderColor = isError ? "#ffccd5" : "#eef2ff";
  }

  // Nav switching (works for anchors or buttons)
  navItems.forEach(item => {
    item.addEventListener("click", (e) => {
      e.preventDefault();
      navItems.forEach(i => i.classList.remove("active"));
      item.classList.add("active");

      const target = item.dataset.target;
      sections.forEach(s => s.classList.add("hidden"));
      const el = document.getElementById(target);
      if (el) el.classList.remove("hidden");

      pageTitle.textContent = item.textContent.trim();

      // If user opened history, load it
      if (target === "history") {
        loadHistory();
      }
    });
  });

  // Load history from server and render
  async function loadHistory() {
    try {
      const res = await fetch("/history");
      if (!res.ok) throw new Error("Failed to fetch history");
      const payload = await res.json();
      const arr = payload.history || [];

      const container = historySection.querySelector(".card");
      // clear existing content except header
      const header = container.querySelector("h2");
      container.innerHTML = "";
      container.appendChild(header);

      if (arr.length === 0) {
        const p = document.createElement("p");
        p.textContent = "No uploaded invoices yet.";
        container.appendChild(p);
        return;
      }

      // render list
      const list = document.createElement("div");
      list.style.marginTop = "12px";
      arr.forEach(item => {
        const row = document.createElement("div");
        row.style.padding = "12px";
        row.style.borderBottom = "1px solid #f0f2ff";
        row.style.display = "flex";
        row.style.justifyContent = "space-between";
        row.style.alignItems = "center";

        const left = document.createElement("div");
        left.innerHTML = `<strong>${escapeHtml(item.filename)}</strong><div style="font-size:13px;color:#6b7280;">${new Date(item.uploaded_at).toLocaleString()}</div>`;

        const right = document.createElement("div");
        const dl = document.createElement("a");
        dl.href = item.excel_file;
        dl.textContent = "Download Excel";
        dl.className = "btn secondary";
        dl.style.textDecoration = "none";
        dl.style.marginLeft = "8px";
        right.appendChild(dl);

        row.appendChild(left);
        row.appendChild(right);
        list.appendChild(row);
      });

      container.appendChild(list);
    } catch (err) {
      console.error(err);
      // keep a simple message in the history card
      const container = historySection.querySelector(".card");
      container.innerHTML = "<h2>📂 Upload History</h2><p>Error loading history.</p>";
    }
  }

  // Upload handling
  uploadForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!fileInput.files || fileInput.files.length === 0) {
      showResponse("❗ Please select a PDF file first.", true);
      return;
    }
    const file = fileInput.files[0];
    if (file.size > 30 * 1024 * 1024) { // 30MB limit
      showResponse("❗ File too large (max 30MB).", true);
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    showResponse("⏳ Uploading and processing... please wait.");
    downloadBtn.disabled = true;

    try {
      const resp = await fetch("/upload-invoice", { method: "POST", body: formData });
      if (!resp.ok) {
        const txt = await resp.text();
        throw new Error(txt || `${resp.status} ${resp.statusText}`);
      }
      const data = await resp.json();

      let html = `<div><strong>✅ ${escapeHtml(data.message || "Uploaded")}</strong></div>`;
      html += `<div style="margin-top:8px;"><small>File: ${escapeHtml(data.filename || "uploaded.pdf")}</small></div>`;

      if (data.excel_file) {
        // enable download
        downloadBtn.disabled = false;
        downloadBtn.onclick = () => { window.location = data.excel_file; };
        html += `<div style="margin-top:10px;"><a href="${data.excel_file}" class="btn secondary" download>📥 Download Excel</a></div>`;
      }

      showResponse(html);
      // refresh history to show the new upload
      await loadHistory();
    } catch (err) {
      console.error(err);
      showResponse("❌ Error uploading file. See console for details.", true);
    }
  });

  // Escape helper
  function escapeHtml(unsafe = "") {
    return String(unsafe)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  // initial load: show upload section and load history quietly
  document.getElementById("upload").classList.remove("hidden");
  loadHistory(); // prefetch history so when user clicks it appears instantly
});
