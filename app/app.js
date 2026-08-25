// JA-GALI — PWA (Faz 1.8/1.9)
// Login senp + chat ki rele backend /chat sèlman (Faz 1.7 fizyone anndan).

const API_URL = "http://192.168.15.13:8000"; // chanje sa nan Faz 7 (deplwaman)
const KLE_STOKAJ = "ja-gali-kòd-aksè";

// ── Referans eleman HTML ──────────────────────────────────────────────

const pajLogin = document.getElementById("paj-login");
const pajChat = document.getElementById("paj-chat");
const fòmLogin = document.getElementById("fòm-login");
const chanKòd = document.getElementById("chan-kòd");
const erèLogin = document.getElementById("erè-login");
const fòmChat = document.getElementById("fòm-chat");
const chanMesaj = document.getElementById("chan-mesaj");
const lisMesaj = document.getElementById("lis-mesaj");
const boutonDekonekte = document.getElementById("bouton-dekonekte");

// ── Jesyon paj (montre/kache) ──────────────────────────────────────────

function montre_paj_chat() {
  pajLogin.classList.add("kache");
  pajChat.classList.remove("kache");
  chanMesaj.focus();
}

function montre_paj_login() {
  pajChat.classList.add("kache");
  pajLogin.classList.remove("kache");
  chanKòd.focus();
}

// ── Ajoute yon mesaj nan lis chat la ───────────────────────────────────

function ajoute_mesaj(tèks, kalite) {
  const div = document.createElement("div");
  div.className = `mesaj mesaj-${kalite}`;
  div.textContent = tèks;
  lisMesaj.appendChild(div);
  lisMesaj.scrollTop = lisMesaj.scrollHeight;
  return div;
}

// ── Apèl API /chat ─────────────────────────────────────────────────────

async function voye_mesaj_bay_backend(mesaj) {
  const kòd = localStorage.getItem(KLE_STOKAJ);

  const repons = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Access-Code": kòd,
    },
    body: JSON.stringify({ message: mesaj }),
  });

  if (repons.status === 401) {
    // Kòd pa valid ankò — retounen nan login
    localStorage.removeItem(KLE_STOKAJ);
    montre_paj_login();
    erèLogin.textContent = "Sesyon ekspire — antre kòd la ankò.";
    throw new Error("401 Unauthorized");
  }

  if (!repons.ok) {
    throw new Error(`Erè sèvè: ${repons.status}`);
  }

  const done_json = await repons.json();
  return done_json.response;
}

// ── Verifye kòd la mache (apèl tès /sante, ki pa pwoteje) ──────────────

async function verifye_kòd_valid(kòd) {
  // /sante pa pwoteje, kidonk nou fè yon senp tès sou /chat ak yon mesaj vid
  // pou konfirme kòd la aksepte san bezwen kreye yon woutt tès separe.
  const repons = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Access-Code": kòd,
    },
    body: JSON.stringify({ message: "" }),
  });
  return repons.status !== 401;
}

// ── Evènman: soumèt login ──────────────────────────────────────────────

fòmLogin.addEventListener("submit", async (evenman) => {
  evenman.preventDefault();
  erèLogin.textContent = "";

  const kòd = chanKòd.value.trim();
  if (!kòd) return;

  const bouton = fòmLogin.querySelector("button");
  bouton.disabled = true;
  bouton.textContent = "...";

  try {
    const valid = await verifye_kòd_valid(kòd);
    if (!valid) {
      erèLogin.textContent = "❌ Kòd aksè envalid.";
      return;
    }

    localStorage.setItem(KLE_STOKAJ, kòd);
    montre_paj_chat();
  } catch (err) {
    erèLogin.textContent = "❌ Backend pa reponn. Verifye li ap kouri.";
  } finally {
    bouton.disabled = false;
    bouton.textContent = "Antre";
  }
});

// ── Evènman: soumèt mesaj chat ──────────────────────────────────────────

fòmChat.addEventListener("submit", async (evenman) => {
  evenman.preventDefault();

  const mesaj = chanMesaj.value.trim();
  if (!mesaj) return;

  ajoute_mesaj(mesaj, "itilizatè");
  chanMesaj.value = "";

  const bul_chajman = ajoute_mesaj("...", "chajman");

  try {
    const repons = await voye_mesaj_bay_backend(mesaj);
    bul_chajman.remove();
    ajoute_mesaj(repons, "backend");
  } catch (err) {
    bul_chajman.remove();
    if (err.message !== "401 Unauthorized") {
      ajoute_mesaj("⚠️ Erè: mesaj la pa pase. Eseye ankò.", "backend");
    }
  }
});

// ── Evènman: dekonekte ───────────────────────────────────────────────

boutonDekonekte.addEventListener("click", () => {
  localStorage.removeItem(KLE_STOKAJ);
  lisMesaj.innerHTML = "";
  montre_paj_login();
});

// ── Enisyalizasyon: si gen kòd deja estoke, antre dirèkteman ───────────

(async function enisyalize() {
  const kòd_estoke = localStorage.getItem(KLE_STOKAJ);

  if (kòd_estoke) {
    try {
      const valid = await verifye_kòd_valid(kòd_estoke);
      if (valid) {
        montre_paj_chat();
        return;
      }
      localStorage.removeItem(KLE_STOKAJ);
    } catch (err) {
      // Backend pa reponn — kite moun nan sou login ak mesaj klè
    }
  }

  montre_paj_login();
})();
