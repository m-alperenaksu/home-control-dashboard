let visible = true;

const TEMP_MIN = 18;
const TEMP_MAX = 30;
const HUM_MIN  = 30;
const HUM_MAX  = 70;

async function fetchData() {
  if (!visible) return;

  try {
    const res  = await fetch("http://localhost:5000");
    const data = await res.json();

    if (data.temp !== null) {
      document.getElementById("tempVal").textContent = data.temp;
      checkThreshold("tempCard", data.temp, TEMP_MIN, TEMP_MAX, "Temperature", "°C");
    }

    if (data.hum !== null) {
      document.getElementById("humVal").textContent = data.hum;
      checkThreshold("humCard", data.hum, HUM_MIN, HUM_MAX, "Humidity", "%");
    }

    document.getElementById("statusBadge").textContent = "Connected";
    document.getElementById("statusBadge").className   = "badge bg-success";
  } catch (e) {
    document.getElementById("statusBadge").textContent = "Disconnected";
    document.getElementById("statusBadge").className   = "badge bg-danger";
  }
}

function checkThreshold(cardId, value, min, max, label, unit) {
  const card = document.getElementById(cardId);

  if (value < min || value > max) {
    const msg = value < min
      ? `${label} too low: ${value}${unit} (min: ${min}${unit})`
      : `${label} too high: ${value}${unit} (max: ${max}${unit})`;

    showAlert(msg);
    card.classList.add("border-danger");
  } else {
    card.classList.remove("border-danger");
  }
}

function showAlert(msg) {
  const box = document.getElementById("alertBox");
  document.getElementById("alertText").textContent = "⚠️ " + msg;
  box.classList.remove("d-none");
}

function closeAlert() {
  document.getElementById("alertBox").classList.add("d-none");
}

function toggleData(checked) {
  visible = checked;

  document.getElementById("tempVal").textContent = "--";
  document.getElementById("humVal").textContent  = "--";

  if (checked) fetchData();
}

fetchData();
setInterval(fetchData, 3000);
