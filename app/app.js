// JA-GALI — PWA (Faz 1.8/1.9)
// Login senp + chat ki rele backend /chat sèlman (Faz 1.7 fizyone anndan).

const API_URL = "https://gali.up.railway.app"; // Railway backend URL
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
const boutonAlèt = document.getElementById("bouton-alèt");
const boutonRapò = document.getElementById("bouton-rapò");
const boutonTounenChat = document.getElementById("bouton-tounen-chat");
const pajAlèt = document.getElementById("paj-alèt");
const lisAlèt = document.getElementById("lis-alèt");

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

// ── Faz 4.4: Paj Alèt ────────────────────────────────────────────────

function fòmate_dat_ayisyen(dat_iso) {
  // "2026-08-30" → "30/08/2026"
  const [a, m, j] = dat_iso.split("-");
  return `${j}/${m}/${a}`;
}

async function chaje_alèt() {
  lisAlèt.innerHTML = '<p class="mesaj-chajman-alèt">Chajman...</p>';
  const kòd = localStorage.getItem(KLE_STOKAJ);

  try {
    const repons = await fetch(`${API_URL}/alèt?jou=90`, {
      headers: { "X-Access-Code": kòd },
    });

    if (!repons.ok) {
      throw new Error(`Erè sèvè: ${repons.status}`);
    }

    const done_json = await repons.json();
    const evènman_yo = done_json.evènman || [];

    if (evènman_yo.length === 0) {
      lisAlèt.innerHTML = '<p class="alèt-vid">✅ Pa gen delè nan 30 pwochen jou yo.</p>';
      return;
    }

    lisAlèt.innerHTML = "";
    evènman_yo.forEach((ev) => {
      const kat = document.createElement("div");
      kat.className = "kat-alèt";
      kat.innerHTML = `
        <div class="tit-alèt">${ev.tit}</div>
        <div class="dat-alèt">${fòmate_dat_ayisyen(ev.dat)}</div>
      `;
      lisAlèt.appendChild(kat);
    });
  } catch (err) {
    lisAlèt.innerHTML = '<p class="alèt-vid">⚠️ Pa ka chaje alèt yo. Verifye backend la ap kouri.</p>';
  }
}

boutonAlèt.addEventListener("click", () => {
  pajChat.classList.add("kache");
  pajAlèt.classList.remove("kache");
  chaje_alèt();
});

boutonTounenChat.addEventListener("click", () => {
  pajAlèt.classList.add("kache");
  pajChat.classList.remove("kache");
});

// ── Faz 6.4: Bouton "Jenere Rapò" ──────────────────────────────────

boutonRapò.addEventListener("click", async () => {
  if (pajChat.classList.contains("kache")) return; // sèlman aji si nou nan chat la

  const bul_chajman = ajoute_mesaj("📄 Ap jenere rapò a (sa ka pran kèk segond)...", "chajman");
  boutonRapò.disabled = true;

  try {
    const kòd = localStorage.getItem(KLE_STOKAJ);
    const repons = await fetch(`${API_URL}/rapò?mwa=3`, {
      method: "POST",
      headers: { "X-Access-Code": kòd },
    });

    bul_chajman.remove();

    if (repons.status === 401) {
      localStorage.removeItem(KLE_STOKAJ);
      montre_paj_login();
      erèLogin.textContent = "Sesyon ekspire — antre kòd la ankò.";
      return;
    }

    if (!repons.ok) {
      const erè_json = await repons.json().catch(() => ({}));
      throw new Error(erè_json.detail || `Erè sèvè: ${repons.status}`);
    }

    // Repons lan se yon fichye PDF (blob), pa JSON — deklannche telechajman
    const blob = await repons.blob();
    const antèt_disposition = repons.headers.get("Content-Disposition") || "";
    const matche_non = antèt_disposition.match(/filename="?([^"]+)"?/);
    const non_fichye = matche_non ? matche_non[1] : "rapo.pdf";

    const url = window.URL.createObjectURL(blob);
    const lyen_a = document.createElement("a");
    lyen_a.href = url;
    lyen_a.download = non_fichye;
    document.body.appendChild(lyen_a);
    lyen_a.click();
    lyen_a.remove();
    window.URL.revokeObjectURL(url);

    ajoute_mesaj(`✅ Rapò "${non_fichye}" telechaje!`, "backend");
  } catch (err) {
    bul_chajman.remove();
    ajoute_mesaj(`⚠️ Erè pandan jenerasyon rapò a: ${err.message}`, "backend");
  } finally {
    boutonRapò.disabled = false;
  }
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

// ── Faz 5.4: Paj Caption ─────────────────────────────────────────────

const boutonCaption = document.getElementById("bouton-caption");
const boutonTounenChatCap = document.getElementById("bouton-tounen-chat-caption");
const pajCaption = document.getElementById("paj-caption");
const fòmCaption = document.getElementById("fòm-caption");
const chanNonPiblikasyon = document.getElementById("chan-non-piblikasyon");
const boutonMandeCaption = document.getElementById("bouton-mande-caption");
const zònRezilta = document.getElementById("zòn-rezilta-caption");
const tèksCaption = document.getElementById("tèks-caption");
const boutonAksepte = document.getElementById("bouton-aksepte-caption");
const boutonRechaje = document.getElementById("bouton-rechaje-caption");
const konfirmasyon = document.getElementById("konfirmasyon-caption");
const estatiCaption = document.getElementById("estati-caption");

// Navige ale nan paj Caption
boutonCaption.addEventListener("click", () => {
  pajChat.classList.add("kache");
  pajCaption.classList.remove("kache");
  chanNonPiblikasyon.focus();
  // Reyinisyalize afichaj la
  zònRezilta.classList.add("kache");
  konfirmasyon.classList.add("kache");
  estatiCaption.textContent = "";
});

// Navige tounen nan chat
boutonTounenChatCap.addEventListener("click", () => {
  pajCaption.classList.add("kache");
  pajChat.classList.remove("kache");
});

// ── Fonksyon: mande caption pou yon non piblikasyon ──────────────────

async function mande_caption(non_piblikasyon) {
  estatiCaption.textContent = "⏳ Ap chèche nan Notion + Drive, epi ap jenere caption…";
  boutonMandeCaption.disabled = true;
  zònRezilta.classList.add("kache");
  konfirmasyon.classList.add("kache");

  try {
    const kòd = localStorage.getItem(KLE_STOKAJ);
    const repons = await fetch(`${API_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Access-Code": kòd,
      },
      body: JSON.stringify({ message: `caption pou ${non_piblikasyon}` }),
    });

    if (repons.status === 401) {
      localStorage.removeItem(KLE_STOKAJ);
      pajCaption.classList.add("kache");
      montre_paj_login();
      erèLogin.textContent = "Sesyon ekspire — antre kòd la ankò.";
      return;
    }

    if (!repons.ok) throw new Error(`Erè sèvè: ${repons.status}`);

    const done_json = await repons.json();
    const tèks = done_json.response;

    estatiCaption.textContent = "";

    // Ekstrè jis tèks caption la (retire prefiks backend la si li prezan)
    // Backend retounen: "📝 Caption pou 'X' (N imaj jwenn):\n\n<caption>"
    const separatè = tèks.indexOf(":\n\n");
    const tèks_caption_sèl = separatè !== -1
      ? tèks.slice(separatè + 3).trim()
      : tèks;

    tèksCaption.textContent = tèks_caption_sèl;
    zònRezilta.classList.remove("kache");

  } catch (err) {
    estatiCaption.textContent = `⚠️ Erè: ${err.message}. Verifye backend la ap kouri.`;
  } finally {
    boutonMandeCaption.disabled = false;
  }
}

// ── Evènman: soumèt fòm Caption ──────────────────────────────────────

fòmCaption.addEventListener("submit", async (evenman) => {
  evenman.preventDefault();
  const non = chanNonPiblikasyon.value.trim();
  if (!non) return;
  await mande_caption(non);
});

// ── Bouton "Aksepte" — kopye + anrejistre nan Notion ─────────────────

boutonAksepte.addEventListener("click", async () => {
  const tèks = tèksCaption.textContent;
  const non_pib = chanNonPiblikasyon.value.trim();
  if (!tèks || !non_pib) return;

  // 1) Kopye nan pwen-presse (menm konpòtman ak anvan)
  try {
    await navigator.clipboard.writeText(tèks);
  } catch (_) {
    const sel = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(tèksCaption);
    sel.removeAllRanges();
    sel.addRange(range);
  }

  konfirmasyon.classList.remove("kache");
  setTimeout(() => konfirmasyon.classList.add("kache"), 3000);

  // 2) Anrejistre nan kolòn "Caption" Notion an (Faz 5.4 amelyore)
  boutonAksepte.disabled = true;
  try {
    const kòd = localStorage.getItem(KLE_STOKAJ);
    const repons = await fetch(`${API_URL}/caption/aksepte`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Access-Code": kòd,
      },
      body: JSON.stringify({ non_piblikasyon: non_pib, caption: tèks }),
    });

    if (!repons.ok) {
      const erè_json = await repons.json().catch(() => ({}));
      throw new Error(erè_json.detail || `Erè sèvè: ${repons.status}`);
    }

    estatiCaption.textContent = "✅ Caption anrejistre nan Notion tou.";
  } catch (err) {
    estatiCaption.textContent = `⚠️ Kopye reyisi, men echwe anrejistre nan Notion: ${err.message}`;
  } finally {
    boutonAksepte.disabled = false;
  }
});

// ── Bouton "Nouvo vèsyon" — mande yon lòt caption ────────────────────

boutonRechaje.addEventListener("click", async () => {
  const non = chanNonPiblikasyon.value.trim();
  if (!non) return;
  await mande_caption(non);
});

// ── Faz 3.5: Paj Payroll ─────────────────────────────────────────────

const boutonPayroll = document.getElementById("bouton-payroll");
const boutonTounenChatPayroll = document.getElementById("bouton-tounen-chat-payroll");
const pajPayroll = document.getElementById("paj-payroll");
const lisPayroll = document.getElementById("lis-payroll");

async function chaje_payroll() {
  lisPayroll.innerHTML = '<p class="mesaj-chajman-alèt">Ap kalkile payroll la...</p>';
  const kòd = localStorage.getItem(KLE_STOKAJ);

  try {
    const repons = await fetch(`${API_URL}/payroll?mwa=3`, {
      headers: { "X-Access-Code": kòd },
    });

    if (repons.status === 401) {
      localStorage.removeItem(KLE_STOKAJ);
      pajPayroll.classList.add("kache");
      montre_paj_login();
      erèLogin.textContent = "Sesyon ekspire — antre kòd la ankò.";
      return;
    }

    if (!repons.ok) {
      throw new Error(`Erè sèvè: ${repons.status}`);
    }

    const done_json = await repons.json();
    const detay = done_json.data || {};
    const kolaboratè_yo = Object.entries(detay);

    if (kolaboratè_yo.length === 0) {
      lisPayroll.innerHTML = '<p class="alèt-vid">✅ Pa gen payroll pou peryòd sa a.</p>';
      return;
    }

    lisPayroll.innerHTML = "";
    kolaboratè_yo.forEach(([non, montan]) => {
      // Afiche sèlman moun ki gen yon montan ki pi gwo pase 0
      if (montan > 0) {
        const kat = document.createElement("div");
        kat.className = "kat-payroll";

        // Fòmate lajan an avèk vigil olye de pwen (opsyonèl)
        const lajan_fòmate = montan.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');

        kat.innerHTML = `
          <div class="info-payroll">
            <span class="non-kolaboratè">👤 ${non}</span>
          </div>
          <div class="montan-payroll">$${lajan_fòmate}</div>
        `;
        lisPayroll.appendChild(kat);
      }
    });

    if (lisPayroll.innerHTML === "") {
      lisPayroll.innerHTML = '<p class="alèt-vid">✅ Pa gen payroll aktif pou peryòd sa a.</p>';
    }
  } catch (err) {
    lisPayroll.innerHTML = '<p class="alèt-vid">⚠️ Pa ka chaje payroll la. Verifye backend la ap kouri.</p>';
  }
}

boutonPayroll.addEventListener("click", () => {
  pajChat.classList.add("kache");
  pajPayroll.classList.remove("kache");
  chaje_payroll();
});

boutonTounenChatPayroll.addEventListener("click", () => {
  pajPayroll.classList.add("kache");
  pajChat.classList.remove("kache");
});

// ── Popup Gid Kòmand ──────────────────────────────────────────────────

const boutonGid = document.getElementById("bouton-gid");
const boutonFèmenGid = document.getElementById("bouton-fèmen-gid");
const modalGid = document.getElementById("modal-gid");

boutonGid.addEventListener("click", () => {
  modalGid.classList.remove("kache");
});

boutonFèmenGid.addEventListener("click", () => {
  modalGid.classList.add("kache");
});

// Fèmen si klike deyò kat la (sou fon nwa a)
modalGid.addEventListener("click", (evenman) => {
  if (evenman.target === modalGid) {
    modalGid.classList.add("kache");
  }
});
