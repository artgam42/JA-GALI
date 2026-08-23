// JA-GALI — PWA
// Faz 0 : jis yon tès konfimasyon ke frontend la ka rele backend la.
// Woutt/lojik reyèl (chat, login, elatriye) ap vin nan Faz 1.

const API_URL = "http://localhost:8000"; // chanje sa nan Faz 6 (deplwaman)

async function verifyeBackend() {
  const elStatut = document.getElementById("statut-backend");
  try {
    const res = await fetch(`${API_URL}/sante`);
    const done = await res.json();
    elStatut.textContent = done.kle_claude_konfigire
      ? "✅ Backend ap kouri, kle Claude konfigire"
      : "⚠️ Backend ap kouri, men kle Claude PA konfigire";
  } catch (err) {
    elStatut.textContent = "❌ Backend pa reponn (limen l ak: uvicorn main:app --reload)";
  }
}

verifyeBackend();
