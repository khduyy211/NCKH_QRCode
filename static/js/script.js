// ====== SCRIPT.JS ======
document.getElementById("searchBtn").addEventListener("click", () => {
    const query = document.getElementById("searchInput").value.trim();
    if (query) {
        alert(`Đang tìm kiếm: "${query}"`);
    } else {
        alert("Vui lòng nhập từ khóa để tìm kiếm!");
    }
});
document.addEventListener("DOMContentLoaded", () => {
    const adminButton = document.getElementById("btnAdmin");

    if (adminButton) {
        adminButton.addEventListener("click", () => {
            // Giả lập kiểm tra quyền truy cập, có thể mở rộng logic đăng nhập ở đây
            window.location.href = "admin.html"; // Chuyển trang sang admin.html
        });
    }
});

      // delegate click on shelf faces
      document.querySelectorAll(".shelf-face").forEach((el) => {
        el.addEventListener("click", () => openShelfModal(el));
        el.addEventListener("keydown", (e) => {
          if (e.key === "Enter" || e.key === " ") openShelfModal(el);
        });
      });

      const shelfModal = new bootstrap.Modal(
        document.getElementById("shelfModal")
      );
      const shelfInfoEl = document.getElementById("shelfInfo");
      const bookListEl = document.getElementById("bookList");
      const sampleBooksWrap = document.getElementById("sampleBooks");

      function openShelfModal(el) {
        const id = el.getAttribute("data-id") || "Không rõ";
        const info = el.getAttribute("data-info") || "";
        document.getElementById("shelfModalLabel").textContent =
          "Mặt kệ: " + id;
        shelfInfoEl.textContent = info;

        // sample dynamic content: pretend top 3
        const sample = [
          `${id} — Tên sách A`,
          `${id} — Tên sách B`,
          `${id} — Tên sách C`,
        ];
        bookListEl.innerHTML = "";
        sample.forEach((s) => {
          const li = document.createElement("li");
          li.textContent = s;
          bookListEl.appendChild(li);
        });
        sampleBooksWrap.style.display = "block";
        shelfModal.show();

        // highlight the clicked shelf briefly
        el.style.boxShadow = "0 18px 34px rgba(11,69,201,0.28)";
        setTimeout(() => (el.style.boxShadow = ""), 900);
      }

      // legend button
      document.getElementById("legendBtn").addEventListener("click", () => {
        alert(
          "Chú giải:\\n- Ô đen: Mặt kệ (click để xem chi tiết)\\n- Dải xanh: Lối đi / đường phân cách"
        );
      });

      // simple search to highlight matching shelf IDs or info
      function doSearch() {
        const q = document
          .getElementById("globalSearch")
          .value.trim()
          .toLowerCase();
        if (!q) {
          resetHighlights();
          return;
        }
        const faces = document.querySelectorAll(".shelf-face");
        let found = false;
        faces.forEach((f) => {
          const id = (f.getAttribute("data-id") || "").toLowerCase();
          const info = (f.getAttribute("data-info") || "").toLowerCase();
          if (id.includes(q) || info.includes(q)) {
            f.style.outline = "3px solid rgba(11,69,201,0.26)";
            f.style.outlineOffset = "4px";
            found = true;
            f.scrollIntoView({ block: "center", behavior: "smooth" });
          } else {
            f.style.outline = "";
          }
        });
        if (!found) alert("Không tìm thấy mặt kệ phù hợp: " + q);
      }

      function resetHighlights() {
        document.querySelectorAll(".shelf-face").forEach((f) => {
          f.style.outline = "";
        });
        document.getElementById("globalSearch").value = "";
      }

      // optional: locate button action inside modal
      document.getElementById("locateBtn").addEventListener("click", () => {
        alert(
          "Chức năng đánh dấu vị trí sẽ hỗ trợ trong bản tích hợp tiếp theo."
        );
      });
