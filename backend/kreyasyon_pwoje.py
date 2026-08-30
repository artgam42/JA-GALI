"""
JA-GALI — Faz 1.6 : Kreyasyon pwojè konplè

Konbine Faz 1.5 (ekstraksyon Claude), 1.4 (kòd pwojè), 1.3 (ekri
Sheets), ak Faz 2.3 (notifikasyon Discord) — yon sèl mesaj natirèl
kreye yon pwojè konplè bout an bout.
"""

from datetime import date


def pwosè_nouvo_pwoje(mesaj: str) -> str:
    """
    Woutin konplè: ekstrè done ak Claude → detèmine kalite kliyan →
    jenere kòd → ekri liy nan Sheets → voye notifikasyon Discord.

    Retounen yon mesaj tèks pou reponn bay itilizatè a (swa yon
    konfimasyon siksè, swa yon kesyon si enfo manke, swa yon erè).
    """
    from ekstraksyon import ekstrè_pwoje, EkstraksyonErreur

    try:
        rezilta_ekstraksyon = ekstrè_pwoje(mesaj)
    except EkstraksyonErreur as e:
        return f"⚠️ Erè pandan konprann mesaj la: {e}"

    if not rezilta_ekstraksyon["pare"]:
        return rezilta_ekstraksyon["kesyon"]

    kliyan = rezilta_ekstraksyon["kliyan"]
    tip_travay = rezilta_ekstraksyon["tip_travay"]
    infos = rezilta_ekstraksyon["infos"]
    delè = rezilta_ekstraksyon["delè"]
    kolaboratè = rezilta_ekstraksyon["kolaboratè"]
    montan = rezilta_ekstraksyon["montan"]
    peye = rezilta_ekstraksyon["peye"]

    if not kliyan or not tip_travay or montan <= 0:
        return (
            "⚠️ Mwen pa jwenn ase enfo pou kreye pwojè a (kliyan, tip travay, "
            "oswa montan manke oswa envalid). Tanpri bay plis detay."
        )

    from kod_pwoje import detèmine_kalite_kliyan, jenere_kòd, KliyanPaNanListeErreur
    from sheets_service import li_liy, ekri_antre_pwoje

    kalite = detèmine_kalite_kliyan(kliyan)

    # Deskripsyon Sheets yo (kòlòn E) pou konte lèt sekans yo
    liy_deskripsyon = li_liy("E:E")
    deskripsyon_egziste = [liy[0] for liy in liy_deskripsyon if liy]

    try:
        rezilta_kòd = jenere_kòd(kalite, kliyan, deskripsyon_egziste, dat=date.today())
    except KliyanPaNanListeErreur as e:
        return f"⚠️ {e}"

    kòd = rezilta_kòd["kòd"]
    avètisman = rezilta_kòd["avètisman"]

    description = f"{kòd} : {tip_travay} - {infos}"

    ekri_antre_pwoje(
        dat=date.today().strftime("%d/%m/%Y"),
        type_operat="Revni",
        kliyan=kliyan,
        categorie="Revni Sèvis",
        description=description,
        montan=montan,
        payer=peye,
        kolaboratè=kolaboratè,
    )

    # Faz 2.3 — premye notifikasyon Discord
    from discord_service import voye_notifikasyon_san_kraze
    from sheets_service import estoke_message_id

    message_id = voye_notifikasyon_san_kraze(kòd, tip_travay, infos, delè, kolaboratè)
    if message_id:
        estoke_message_id(kòd, message_id)
        estati_discord = "✅ Notifikasyon Discord voye."
    else:
        estati_discord = (
            "⚠️ Notifikasyon Discord echwe (verifye webhook nan .env), "
            "men pwojè a kreye nan Sheets san pwoblèm."
        )

    mesaj_avètisman = f"\n{avètisman}" if avètisman else ""

    return (
        f"✅ Pwojè kreye: **{kòd}**\n"
        f"Kliyan: {kliyan} | Montan: {montan} goud | Peye: {peye} goud\n"
        f"{estati_discord}{mesaj_avètisman}"
    )
