const chatBox = document.getElementById("chat-box");
const input = document.getElementById("input");

const infoBtn = document.getElementById("infoBtn");
const jaSection = document.getElementById("ja-section");

let isOpen = false;

// 日本語説明の表示/非表示
infoBtn.addEventListener("click", () => {
  isOpen = !isOpen;
  jaSection.style.display = isOpen ? "block" : "none";
});

// メッセージ追加
function addMessage(role, text) {
  const div = document.createElement("div");
  div.classList.add("message", role);
  div.innerText = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

// API送信
function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  // ユーザーメッセージ表示
  addMessage("user", text);

  // 入力欄クリア
  input.value = "";

  fetch("/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      message: text
    })
  })
    .then(res => res.json())
    .then(data => {
      // Bot の返答表示
      addMessage("bot", data.reply);

      // Learning Area 更新
      document.getElementById("corrected").innerText =
        data.corrected_sentence || "";

      document.getElementById("explanation_en").innerText =
        data.explanation_en || "";

      document.getElementById("explanation_ja").innerText =
        data.explanation_ja || "";
    })
    .catch(err => {
      console.error("Error:", err);
      addMessage("bot", "Error: Failed to get response.");
    });
}

// Enter キーで送信
input.addEventListener("keydown", function (e) {
  if (e.key === "Enter") {
    e.preventDefault();
    sendMessage();
  }
});