const backendURL = "http://localhost:5000";
function feedback(isPositive, btn) {
  if (isPositive) {
    alert(
      "Thank you for your feedback. We'll make sure to generate similar responses in the future."
    );
  } else {
    alert(
      "Thank you for your feedback. We'll make sure to not generate this response again."
    );
  }
  // Delete the entire prompt div
  btn.closest(".prompt-box").remove();
}

setInterval(function () {
  // Fetch new messages every second
  fetch("http://127.0.0.1:5000/check_new_messages")
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      if (JSON.stringify(data) !== "{}") {
		const userText = data["new_message"];
		simulateTypingEffect("transcription", "Client: \n" + userText, true);
        const promptBox = document.createElement("div");
        promptBox.className =
          "prompt-box bg-gray-700 p-5 rounded-xl shadow-lg text-white whitespace-pre-wrap relative";
        promptBox.innerHTML = `
			<p id="prompt" class="typing bg-gray-800 p-2 rounded-xl mb-4"></p>
			<div class="flex justify-center items-center space-x-2 mt-2">
				<span class="text-gray-300 text-sm font-semibold">Was this helpful?</span>
				<button class="thumbs-up bg-green-500 p-2 rounded-full focus:outline-none" onclick="feedback(true, this)">👍</button>
				<button class="thumbs-down bg-red-500 p-2 rounded-full focus:outline-none" onclick="feedback(false, this)">👎</button>
			</div>
			`;
        document.getElementById("prompts").appendChild(promptBox);
        simulateTypingEffect("prompt", data["prompt"].trim());
      }
    })
    .catch(function (err) {});
}, 1000);

setInterval(function () {
  console.log("run");
  // Fetch new messages every second
  fetch("http://127.0.0.1:5000/get_first_line")
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      if (JSON.stringify(data) !== "{}") {
		const userText = data["first_line"];
		simulateTypingEffect("transcription", "Client: \n" + userText, true);
        const promptBox = document.createElement("div");
        promptBox.className =
          "prompt-box bg-gray-700 p-5 rounded-xl shadow-lg text-white whitespace-pre-wrap relative";
        promptBox.innerHTML = `
			<p id="prompt" class="typing bg-gray-800 p-2 rounded-xl mb-4"></p>
			<div class="flex justify-center items-center space-x-2 mt-2">
				<span class="text-gray-300 text-sm font-semibold">Was this helpful?</span>
				<button class="thumbs-up bg-green-500 p-2 rounded-full focus:outline-none" onclick="feedback(true, this)">👍</button>
				<button class="thumbs-down bg-red-500 p-2 rounded-full focus:outline-none" onclick="feedback(false, this)">👎</button>
			</div>
			`;
        document.getElementById("prompts").appendChild(promptBox);
        simulateTypingEffect("prompt", data["prompt"].trim());
      }
    })
    .catch(function (err) {});
}, 1000);

// Send message to backend when submit is clicked
async function addUserTextToTranscription() {
  const userText = document.querySelector("textarea").value;
  fetch("http://127.0.0.1:5000/send_message", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: userText }),
  });
  simulateTypingEffect("transcription", "You: " + userText, true);
  document.querySelector("textarea").value = ""; // Clear the textarea after adding the text
}

function simulateTypingEffect(elementId, text, append = false) {
  const element = document.getElementById(elementId);
  const words = text.split(" ");
  let currentText = append ? element.textContent : "";
  let currentWidth = 0;

  function typeWord(index) {
    if (index < words.length) {
      const testText = currentText + words[index] + " ";
      element.textContent = testText;
      const lineWidth = element.getBoundingClientRect().width;
      const containerWidth = element.parentNode.getBoundingClientRect().width;

      if (lineWidth > containerWidth && currentText !== "") {
        currentText += "\n" + words[index] + " ";
      } else {
        currentText = testText;
      }

      setTimeout(() => {
        typeWord(index + 1);
      }, 100); // 100ms delay between words
    }
  }

  typeWord(0);
}
