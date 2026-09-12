from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRODUCT = ROOT / "Agenti" / "Ispettore del Bando"
SCRIPT = PRODUCT / "scripts" / "verifica_fascicolo.py"


def load_module():
    assert SCRIPT.exists(), "manca il verificatore deterministico dell'Ispettore del Bando"
    spec = importlib.util.spec_from_file_location("verifica_fascicolo", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def evidence_file(root: Path, name: str = "prova.pdf", content: bytes = b"prova") -> dict[str, str]:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return {
        "id": name,
        "path": name,
        "sha256": hashlib.sha256(content).hexdigest(),
    }


def expense_index(root: Path) -> dict[str, str]:
    invoice_1 = evidence_file(root, "spese/fatture/fattura-1.pdf", b"fattura-1")
    payment_1 = evidence_file(root, "spese/pagamenti/pagamento-1.pdf", b"pagamento-1")
    invoice_2 = evidence_file(root, "spese/fatture/fattura-2.pdf", b"fattura-2")
    payment_2 = evidence_file(root, "spese/pagamenti/pagamento-2.pdf", b"pagamento-2")
    index = root / "indice-spese.csv"
    with index.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=(
                "coppia_id",
                "fattura_path",
                "fattura_sha256",
                "pagamento_path",
                "pagamento_sha256",
                "fornitore_id",
                "numero_fattura",
                "data_fattura",
                "data_pagamento",
                "riferimento_pagamento",
                "importo_eur",
                "stato",
                "attesa_controllo_id",
            ),
        )
        writer.writeheader()
        writer.writerow(
            {
                "coppia_id": "1",
                "fattura_path": invoice_1["path"],
                "fattura_sha256": invoice_1["sha256"],
                "pagamento_path": payment_1["path"],
                "pagamento_sha256": payment_1["sha256"],
                "fornitore_id": "IT00000000001",
                "numero_fattura": "F-1",
                "data_fattura": "2026-07-08",
                "data_pagamento": "2026-07-08",
                "riferimento_pagamento": "PAY-1",
                "importo_eur": "40.00",
                "stato": "AMMESSA",
                "attesa_controllo_id": "",
            }
        )
        writer.writerow(
            {
                "coppia_id": "2",
                "fattura_path": invoice_2["path"],
                "fattura_sha256": invoice_2["sha256"],
                "pagamento_path": payment_2["path"],
                "pagamento_sha256": payment_2["sha256"],
                "fornitore_id": "IT00000000001",
                "numero_fattura": "F-2",
                "data_fattura": "2026-07-09",
                "data_pagamento": "2026-07-09",
                "riferimento_pagamento": "PAY-2",
                "importo_eur": "60.00",
                "stato": "AMMESSA",
                "attesa_controllo_id": "",
            }
        )
    return {
        "id": "indice-spese",
        "path": index.name,
        "sha256": hashlib.sha256(index.read_bytes()).hexdigest(),
    }


def base_manifest(root: Path) -> dict:
    evidence = evidence_file(root)
    expenses = expense_index(root)
    summary = evidence_file(root, "riepilogo-finale.pdf", b"riepilogo finale")
    return {
        "schema_version": 1,
        "pratica": {
            "nome": "Voucher prova",
            "ente": "Camera di Commercio",
            "edizione": "2026",
            "fase": "firma",
        },
        "fonti_ufficiali": [
            {
                "nome": "Bando e modulistica",
                "url": "https://ente.example/bando",
                "verificata_il": "2026-09-12",
                "stato": "PROVATO",
                "evidenza_id": evidence["id"],
            }
        ],
        "evidenze": [evidence, expenses, summary],
        "controlli": [
            {
                "id": "modulo-domanda",
                "voce": "Modulo domanda completo",
                "stato": "PROVATO",
                "evidenze": [evidence["id"]],
                "azione": "",
            },
            {
                "id": "firma-titolare",
                "voce": "Firma CAdES del titolare",
                "stato": "PASSAGGIO_UMANO",
                "evidenze": [evidence["id"]],
                "azione": "",
                "categoria_umana": "firma",
                "oggetto_evidenza": evidence["id"],
            },
            {
                "id": "output-da-firmare",
                "voce": "Documento finale da firmare verificato",
                "stato": "PROVATO",
                "evidenze": [evidence["id"]],
                "azione": "",
            },
        ],
        "output_finale": {
            "da_firmare_evidenza": evidence["id"],
            "riepilogo_invio_evidenza": summary["id"],
        },
        "spese": {
            "richieste": True,
            "fatture_attese": 2,
            "fatture_trovate": 2,
            "pagamenti_trovati": 2,
            "coppie_verificate": 2,
            "coppie_irrisolte": 0,
            "totale_ammesso_eur": "100.00",
            "totale_escluso_eur": "0.00",
            "indice_csv": expenses["path"],
            "evidenze": [expenses["id"]],
        },
    }


def add_proven_payment(manifest: dict, root: Path) -> None:
    notice = evidence_file(root, "avviso-pagamento.pdf", b"bollo 16 euro BOLLO-2026")
    receipt = evidence_file(root, "ricevuta-pagamento.pdf", b"pagamento eseguito")
    manifest["evidenze"].extend([notice, receipt])
    manifest["controlli"].extend(
        [
            {
                "id": "avviso-pagamento",
                "voce": "Avviso di pagamento verificato",
                "stato": "PROVATO",
                "evidenze": [notice["id"]],
                "azione": "",
            },
            {
                "id": "pagamento-completato",
                "voce": "Pagamento completato",
                "stato": "PROVATO",
                "evidenze": [notice["id"], receipt["id"]],
                "azione": "",
            },
        ]
    )
    manifest["pagamento"] = {
        "richiesto": True,
        "avviso_evidenza": notice["id"],
        "avviso_sha256": notice["sha256"],
        "importo_atteso_eur": "16.00",
        "riferimento_atteso": "BOLLO-2026",
        "ricevuta_evidenza": receipt["id"],
        "fonte_non_richiesto_evidenza": "",
        "importo_eur": "16.00",
        "riferimento": "BOLLO-2026",
        "eseguito_il": "2026-09-12T12:10:00+02:00",
    }


def add_valid_signature(manifest: dict, root: Path) -> None:
    original_id = manifest["output_finale"]["da_firmare_evidenza"]
    original = next(item for item in manifest["evidenze"] if item["id"] == original_id)
    signed = evidence_file(root, "domanda.pdf.p7m", b"cades")
    receipt = evidence_file(root, "verifica-firma.txt", b"firma valida")
    manifest["evidenze"].extend([signed, receipt])
    manifest["controlli"][1] = {
        "id": "firma-titolare",
        "voce": "Firma del titolare applicata",
        "stato": "PROVATO",
        "evidenze": [signed["id"]],
        "azione": "",
    }
    manifest["controlli"].append(
        {
            "id": "validazione-firma-digitale",
            "voce": "Firma CAdES valida e firmatario corretto",
            "stato": "PROVATO",
            "evidenze": [original_id, signed["id"], receipt["id"]],
            "azione": "",
        }
    )
    manifest["validazione_firma"] = {
        "richiesta": True,
        "formato": "CAdES",
        "firmatario_atteso": "Mario Rossi",
        "firmatario_verificato": "Mario Rossi",
        "originale_evidenza": original_id,
        "originale_sha256": original["sha256"],
        "file_firmato_evidenza": signed["id"],
        "ricevuta_evidenza": receipt["id"],
        "strumento": "verificatore firma installato",
        "verificata_il": "2026-09-12T12:00:00+02:00",
        "esito": "VALIDA",
    }


def add_proven_summary(manifest: dict) -> None:
    summary_id = manifest["output_finale"]["riepilogo_invio_evidenza"]
    manifest["controlli"].append(
        {
            "id": "riepilogo-finale",
            "voce": "Riepilogo finale verificato",
            "stato": "PROVATO",
            "evidenze": [summary_id],
            "azione": "",
        }
    )


def proven_payment_controls(manifest: dict) -> dict[str, dict]:
    return {
        control["id"]: control
        for control in manifest["controlli"]
        if control["id"] in {"avviso-pagamento", "pagamento-completato"}
    }


def test_verdetto_pronto_ammette_solo_i_gesti_umani_riservati(tmp_path: Path):
    module = load_module()
    result = module.valuta(base_manifest(tmp_path), tmp_path)
    assert result["verdetto"] == "PRONTO"
    assert result["passaggi_umani"] == [
        "Il titolare applica la firma digitale al file `prova.pdf`."
    ]
    assert result["blocchi"] == []


def test_conflitto_sostanziale_prevale_sull_attesa_esterna(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    manifest["controlli"].extend(
        [
            {
                "id": "fornitore",
                "voce": "Ammissibilita fornitore",
                "stato": "IN_ATTESA_ESTERNA",
                "evidenze": [],
                "azione": "Attendere risposta scritta dell'ente.",
            },
            {
                "id": "cades",
                "voce": "Prova tecnica CAdES .p7m",
                "stato": "BLOCCO",
                "evidenze": [],
                "azione": "Eseguire e verificare la prova CAdES.",
            },
        ]
    )
    result = module.valuta(manifest, tmp_path)
    assert result["verdetto"] == "BLOCCATO"
    assert result["blocchi"] == ["Eseguire e verificare la prova CAdES."]
    assert result["attese_esterne"] == ["Attendere risposta scritta dell'ente."]


def test_fonte_ufficiale_rifiuta_date_non_valide_o_future(tmp_path: Path):
    module = load_module()
    for invalid_date in ("mai", "2099-01-01"):
        case_root = tmp_path / invalid_date
        case_root.mkdir()
        manifest = base_manifest(case_root)
        manifest["fonti_ufficiali"][0]["verificata_il"] = invalid_date

        result = module.valuta(manifest, case_root)

        assert result["verdetto"] == "BLOCCATO"
        assert "Fonte non provata: Bando e modulistica." in result["blocchi"]


def test_identita_della_pratica_e_versione_schema_sono_obbligatorie(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    manifest["schema_version"] = 99
    manifest["pratica"]["nome"] = ""

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "Versione schema non supportata: usare 1." in result["blocchi"]
    assert "Identita pratica incompleta: nome." in result["blocchi"]


def test_sola_risposta_esterna_mancante_produce_in_attesa(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    manifest["controlli"].append(
        {
            "id": "quesito-ente",
            "voce": "Risposta scritta dell'ente",
            "stato": "IN_ATTESA_ESTERNA",
            "evidenze": [],
            "azione": "Attendere la risposta protocollata.",
        }
    )
    result = module.valuta(manifest, tmp_path)
    assert result["verdetto"] == "IN ATTESA"
    assert result["attese_esterne"] == ["Attendere la risposta protocollata."]
    assert result["prossimo_passaggio_umano"] == ""
    assert "firma digitale" not in module.render_report(manifest, result).lower()


def test_quadratura_spese_incompleta_blocca_anche_se_dichiarata_controllata(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    manifest["spese"]["fatture_attese"] = 352
    manifest["spese"]["fatture_trovate"] = 352
    manifest["spese"]["pagamenti_trovati"] = 352
    manifest["spese"]["coppie_verificate"] = 351
    result = module.valuta(manifest, tmp_path)
    assert result["verdetto"] == "BLOCCATO"
    assert "Quadratura spese incompleta: 351/352 coppie verificate, 0 irrisolte dichiarate." in result["blocchi"]


def test_spese_non_possono_essere_disattivate_senza_deroga_ufficiale(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    manifest["spese"] = {"richieste": False}

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "Spese dichiarate non richieste senza prova sulla fonte ufficiale." in result["blocchi"]


def test_spese_possono_essere_escluse_solo_con_deroga_ufficiale_provata(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    official_id = manifest["fonti_ufficiali"][0]["evidenza_id"]
    manifest["spese"] = {
        "richieste": False,
        "fonte_non_richieste_evidenza": official_id,
    }
    manifest["controlli"].append(
        {
            "id": "spese-non-richieste",
            "voce": "La fonte ufficiale non richiede un fascicolo spese",
            "stato": "PROVATO",
            "evidenze": [official_id],
            "azione": "",
        }
    )

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "PRONTO"
    assert result["blocchi"] == []


def test_indice_ridotto_non_nasconde_documenti_presenti_nelle_cartelle_spese(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    index = tmp_path / manifest["spese"]["indice_csv"]
    rows = list(csv.DictReader(index.read_text(encoding="utf-8").splitlines()))
    with index.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerow(rows[0])
    for evidence in manifest["evidenze"]:
        if evidence["id"] == "indice-spese":
            evidence["sha256"] = hashlib.sha256(index.read_bytes()).hexdigest()
    manifest["spese"].update(
        {
            "cartelle_fatture": ["spese/fatture/selezionate"],
            "cartelle_pagamenti": ["spese/pagamenti/selezionati"],
            "fatture_attese": 1,
            "fatture_trovate": 1,
            "pagamenti_trovati": 1,
            "coppie_verificate": 1,
            "totale_ammesso_eur": "40.00",
        }
    )

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "Inventario fatture: 2 file presenti, 1 indicizzati." in result["blocchi"]
    assert "Inventario pagamenti: 2 file presenti, 1 indicizzati." in result["blocchi"]


def test_inventario_non_ignora_file_con_estensione_diversa(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    (tmp_path / "spese/fatture/fattura-3.xml").write_text("<fattura />", encoding="utf-8")

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "Inventario fatture: 3 file presenti, 2 indicizzati." in result["blocchi"]


def test_inventario_blocca_sottocartelle_collegate_simbolicamente(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    hidden = tmp_path / "archivio-fatture"
    hidden.mkdir()
    (hidden / "fattura-3.pdf").write_bytes(b"fattura-3")
    (tmp_path / "spese/fatture/collegate").symlink_to(hidden, target_is_directory=True)

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert any(
        block.startswith("Inventario fatture: collegamento simbolico non ammesso:")
        for block in result["blocchi"]
    )


def test_stesso_file_non_puo_valere_come_fattura_e_pagamento(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    index = tmp_path / manifest["spese"]["indice_csv"]
    rows = list(csv.DictReader(index.read_text(encoding="utf-8").splitlines()))
    invoice_path = tmp_path / rows[0]["fattura_path"]
    payment_path = tmp_path / rows[0]["pagamento_path"]
    payment_path.write_bytes(invoice_path.read_bytes())
    rows[0]["pagamento_sha256"] = rows[0]["fattura_sha256"]
    with index.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    for evidence in manifest["evidenze"]:
        if evidence["id"] == "indice-spese":
            evidence["sha256"] = hashlib.sha256(index.read_bytes()).hexdigest()

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "Prospetto spese: stesso contenuto usato come fattura e pagamento." in result["blocchi"]


def test_hash_errato_trasforma_la_prova_in_blocco(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    manifest["evidenze"][0]["sha256"] = "0" * 64
    result = module.valuta(manifest, tmp_path)
    assert result["verdetto"] == "BLOCCATO"
    assert result["evidenze_non_valide"] == ["prova.pdf: impronta SHA-256 diversa"]


def test_gesto_umano_generico_non_nasconde_lavoro_dell_agente(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    manifest["controlli"][0] = {
        "id": "ricontrollo",
        "voce": "Ricontrollare i documenti",
        "stato": "PASSAGGIO_UMANO",
        "evidenze": [],
        "azione": "Fabrizio ricontrolla i 704 PDF.",
        "categoria_umana": "controllo-documenti",
    }
    result = module.valuta(manifest, tmp_path)
    assert result["verdetto"] == "BLOCCATO"
    assert "ricontrollo: 'controllo-documenti' non e un gesto riservato al titolare" in result["blocchi"]


def test_invio_non_puo_essere_mascherato_come_scelta_del_titolare(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    manifest["pratica"]["fase"] = "preparazione"
    manifest["controlli"][1] = {
        "id": "invio-mascherato",
        "voce": "Invio definitivo",
        "stato": "PASSAGGIO_UMANO",
        "evidenze": [],
        "azione": "Il titolare invia definitivamente la domanda su ReStart.",
        "categoria_umana": "scelta-titolare",
    }

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "invio-mascherato: identificativo non canonico per scelta-titolare." in result["blocchi"]


def test_conferma_finale_non_puo_passare_come_scelta_strutturata(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    manifest["pratica"]["fase"] = "preparazione"
    manifest["controlli"][1] = {
        "id": "scelta-titolare",
        "voce": "Conferma definitiva nel portale",
        "stato": "PASSAGGIO_UMANO",
        "evidenze": [],
        "azione": "Il titolare clicca Conferma definitiva su ReStart.",
        "categoria_umana": "scelta-titolare",
    }

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert (
        "scelta-titolare: PASSAGGIO_UMANO deve usare campi strutturati, non azione libera."
        in result["blocchi"]
    )


def test_testo_libero_non_rientra_dal_campo_oggetto(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    manifest["pratica"]["fase"] = "preparazione"
    manifest["controlli"][1] = {
        "id": "dichiarazione-titolare",
        "voce": "Dichiarazione del titolare",
        "stato": "PASSAGGIO_UMANO",
        "evidenze": [],
        "azione": "",
        "categoria_umana": "dichiarazione",
        "oggetto": "la domanda e la invia definitivamente sul portale",
    }

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert (
        "dichiarazione-titolare: gesto umano senza oggetto_evidenza integro."
        in result["blocchi"]
    )


def test_dichiarazione_richiede_un_controllo_preparatorio_provato(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    declaration = evidence_file(tmp_path, "dichiarazione.txt", b"testo da confermare")
    manifest["evidenze"].append(declaration)
    manifest["pratica"]["fase"] = "preparazione"
    manifest["controlli"] = [
        manifest["controlli"][0],
        {
            "id": "dichiarazione-titolare",
            "voce": "Dichiarazione del titolare",
            "stato": "PASSAGGIO_UMANO",
            "evidenze": [declaration["id"]],
            "azione": "",
            "categoria_umana": "dichiarazione",
            "oggetto_evidenza": declaration["id"],
        },
    ]

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "dichiarazione-titolare: preparazione non provata sullo stesso oggetto." in result["blocchi"]


def test_scelta_titolare_richiede_domanda_e_da_due_a_cinque_opzioni(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    choice = evidence_file(tmp_path, "scelta.txt", b"una sola opzione")
    manifest["evidenze"].append(choice)
    manifest["pratica"]["fase"] = "preparazione"
    manifest["scelta_titolare"] = {
        "evidenza_id": choice["id"],
        "domanda": "",
        "opzioni": ["Conferma"],
    }
    manifest["controlli"] = [
        manifest["controlli"][0],
        {
            "id": "scelta-da-compiere",
            "voce": "Scelta preparata",
            "stato": "PROVATO",
            "evidenze": [choice["id"]],
            "azione": "",
        },
        {
            "id": "scelta-titolare",
            "voce": "Scelta del titolare",
            "stato": "PASSAGGIO_UMANO",
            "evidenze": [choice["id"]],
            "azione": "",
            "categoria_umana": "scelta-titolare",
            "oggetto_evidenza": choice["id"],
        },
    ]

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "scelta-titolare: domanda o opzioni non valide." in result["blocchi"]


def test_scelta_titolare_normalizza_maiuscole_e_unicode_nelle_opzioni(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    choice = evidence_file(tmp_path, "scelta-duplicata.txt", b"Approva / approva")
    manifest["evidenze"].append(choice)
    manifest["pratica"]["fase"] = "preparazione"
    manifest["scelta_titolare"] = {
        "evidenza_id": choice["id"],
        "domanda": "Quale opzione scegli?",
        "opzioni": ["Approva", "approva"],
    }
    manifest["controlli"] = [
        manifest["controlli"][0],
        {
            "id": "scelta-da-compiere",
            "voce": "Scelta preparata",
            "stato": "PROVATO",
            "evidenze": [choice["id"]],
            "azione": "",
        },
        {
            "id": "scelta-titolare",
            "voce": "Scelta del titolare",
            "stato": "PASSAGGIO_UMANO",
            "evidenze": [choice["id"]],
            "azione": "",
            "categoria_umana": "scelta-titolare",
            "oggetto_evidenza": choice["id"],
        },
    ]

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "scelta-titolare: domanda o opzioni non valide." in result["blocchi"]


def test_accesso_e_2fa_richiedono_preparazione_provata(tmp_path: Path):
    module = load_module()
    for category, control_id in (("accesso", "accesso"), ("2fa", "2fa")):
        case_root = tmp_path / category
        case_root.mkdir()
        manifest = base_manifest(case_root)
        object_id = manifest["evidenze"][0]["id"]
        manifest["pratica"]["fase"] = "preparazione"
        manifest["controlli"] = [
            manifest["controlli"][0],
            {
                "id": control_id,
                "voce": category,
                "stato": "PASSAGGIO_UMANO",
                "evidenze": [object_id],
                "azione": "",
                "categoria_umana": category,
                "oggetto_evidenza": object_id,
            },
        ]

        result = module.valuta(manifest, case_root)

        assert result["verdetto"] == "BLOCCATO"
        assert f"{control_id}: preparazione non provata sullo stesso oggetto." in result["blocchi"]


def test_fase_firma_non_passa_senza_gesto_firma(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    manifest["controlli"] = [manifest["controlli"][0]]

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert result["prossimo_passaggio_umano"] == ""
    assert "Fase firma senza l'unico gesto umano corrente." in result["blocchi"]


def test_firma_deve_riferirsi_all_output_finale_dichiarato(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    invoice = tmp_path / "spese/fatture/fattura-1.pdf"
    invoice_evidence = {
        "id": "fattura-da-firmare",
        "path": str(invoice.relative_to(tmp_path)),
        "sha256": hashlib.sha256(invoice.read_bytes()).hexdigest(),
    }
    manifest["evidenze"].append(invoice_evidence)
    manifest["controlli"][1]["evidenze"] = [invoice_evidence["id"]]
    manifest["controlli"][1]["oggetto_evidenza"] = invoice_evidence["id"]

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "firma-titolare: oggetto diverso dall'output finale da firmare." in result["blocchi"]


def test_output_da_firmare_deve_avere_un_controllo_provato(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    summary_id = manifest["output_finale"]["riepilogo_invio_evidenza"]
    manifest["output_finale"]["da_firmare_evidenza"] = summary_id
    manifest["controlli"][1]["evidenze"] = [summary_id]
    manifest["controlli"][1]["oggetto_evidenza"] = summary_id

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "Output da firmare non provato prima del gesto del titolare." in result["blocchi"]


def test_invio_deve_riferirsi_al_riepilogo_finale_dichiarato(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    invoice = tmp_path / "spese/fatture/fattura-1.pdf"
    invoice_evidence = {
        "id": "fattura-da-inviare",
        "path": str(invoice.relative_to(tmp_path)),
        "sha256": hashlib.sha256(invoice.read_bytes()).hexdigest(),
    }
    manifest["evidenze"].append(invoice_evidence)
    manifest["pratica"]["fase"] = "invio"
    manifest["controlli"][1] = {
        "id": "invio-finale",
        "voce": "Invio definitivo",
        "stato": "PASSAGGIO_UMANO",
        "evidenze": [invoice_evidence["id"]],
        "azione": "",
        "categoria_umana": "invio-finale",
        "oggetto_evidenza": invoice_evidence["id"],
    }

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "invio-finale: oggetto diverso dal riepilogo finale verificato." in result["blocchi"]


def test_riepilogo_finale_non_puo_essere_una_ricevuta_di_pagamento(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    add_valid_signature(manifest, tmp_path)
    add_proven_payment(manifest, tmp_path)
    payment_receipt_id = manifest["pagamento"]["ricevuta_evidenza"]
    manifest["output_finale"]["riepilogo_invio_evidenza"] = payment_receipt_id
    manifest["pratica"]["fase"] = "invio"
    manifest["controlli"].extend(
        [
            {
                "id": "riepilogo-finale",
                "voce": "Riepilogo finale verificato",
                "stato": "PROVATO",
                "evidenze": [payment_receipt_id],
                "azione": "",
            },
            {
                "id": "invio-finale",
                "voce": "Invio definitivo",
                "stato": "PASSAGGIO_UMANO",
                "evidenze": [payment_receipt_id],
                "azione": "",
                "categoria_umana": "invio-finale",
                "oggetto_evidenza": payment_receipt_id,
            },
        ]
    )

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "Riepilogo finale sovrapposto ad avvisi o ricevute." in result["blocchi"]


def test_validazione_firma_deve_continuare_dallo_stesso_output_originale(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    add_valid_signature(manifest, tmp_path)
    manifest["validazione_firma"]["originale_evidenza"] = "indice-spese"
    manifest["validazione_firma"]["originale_sha256"] = manifest["evidenze"][1]["sha256"]
    validation = next(
        control
        for control in manifest["controlli"]
        if control["id"] == "validazione-firma-digitale"
    )
    validation["evidenze"].append("indice-spese")
    manifest["pratica"]["fase"] = "invio"
    add_proven_payment(manifest, tmp_path)
    manifest["controlli"].append(
        {
            "id": "invio-finale",
            "voce": "Invio definitivo",
            "stato": "PASSAGGIO_UMANO",
            "evidenze": ["prova.pdf"],
            "azione": "",
            "categoria_umana": "invio-finale",
            "oggetto_evidenza": "prova.pdf",
        }
    )

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert (
        "Validazione firma digitale non riferita all'output finale originale."
        in result["blocchi"]
    )


def test_validazione_firma_rifiuta_timestamp_senza_data_e_fuso(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    add_valid_signature(manifest, tmp_path)
    manifest["validazione_firma"]["verificata_il"] = "mai"
    manifest["pratica"]["fase"] = "invio"
    add_proven_payment(manifest, tmp_path)
    manifest["controlli"].append(
        {
            "id": "invio-finale",
            "voce": "Invio definitivo",
            "stato": "PASSAGGIO_UMANO",
            "evidenze": ["prova.pdf"],
            "azione": "",
            "categoria_umana": "invio-finale",
            "oggetto_evidenza": "prova.pdf",
        }
    )

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "Validazione firma digitale incompleta: data." in result["blocchi"]


def test_file_firmato_non_puo_valere_come_ricevuta_di_validazione(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    add_valid_signature(manifest, tmp_path)
    signed_id = manifest["validazione_firma"]["file_firmato_evidenza"]
    manifest["validazione_firma"]["ricevuta_evidenza"] = signed_id
    manifest["pratica"]["fase"] = "invio"
    add_proven_payment(manifest, tmp_path)
    manifest["controlli"].append(
        {
            "id": "invio-finale",
            "voce": "Invio definitivo",
            "stato": "PASSAGGIO_UMANO",
            "evidenze": ["prova.pdf"],
            "azione": "",
            "categoria_umana": "invio-finale",
            "oggetto_evidenza": "prova.pdf",
        }
    )

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "Originale, file firmato e ricevuta di validazione devono essere distinti." in result["blocchi"]


def test_il_prospetto_spese_viene_letto_e_il_totale_non_e_autodichiarato(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    manifest["spese"]["totale_ammesso_eur"] = "99.99"
    result = module.valuta(manifest, tmp_path)
    assert result["verdetto"] == "BLOCCATO"
    assert "Totale ammesso dichiarato EUR 99.99, calcolato dal prospetto EUR 100.00." in result["blocchi"]


def test_il_prospetto_spese_rifiuta_importi_non_finiti(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    index = tmp_path / manifest["spese"]["indice_csv"]
    rows = list(csv.DictReader(index.read_text(encoding="utf-8").splitlines()))
    rows[0]["importo_eur"] = "Infinity"
    with index.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    for evidence in manifest["evidenze"]:
        if evidence["id"] == "indice-spese":
            evidence["sha256"] = hashlib.sha256(index.read_bytes()).hexdigest()

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "Prospetto spese: importo_eur non valido alla riga 2." in result["blocchi"]


def test_il_prospetto_spese_blocca_coppie_duplicate(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    index = tmp_path / manifest["spese"]["indice_csv"]
    rows = list(csv.DictReader(index.read_text(encoding="utf-8").splitlines()))
    rows[1]["coppia_id"] = rows[0]["coppia_id"]
    with index.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    for evidence in manifest["evidenze"]:
        if evidence["id"] == "indice-spese":
            evidence["sha256"] = hashlib.sha256(index.read_bytes()).hexdigest()
    result = module.valuta(manifest, tmp_path)
    assert result["verdetto"] == "BLOCCATO"
    assert "Prospetto spese: coppia_id duplicato alla riga 3: 1." in result["blocchi"]


def test_il_prospetto_spese_normalizza_i_percorsi_prima_dei_duplicati(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    index = tmp_path / manifest["spese"]["indice_csv"]
    rows = list(csv.DictReader(index.read_text(encoding="utf-8").splitlines()))
    rows[1]["fattura_path"] = "spese/fatture/sottocartella/../fattura-1.pdf"
    rows[1]["fattura_sha256"] = rows[0]["fattura_sha256"]
    (tmp_path / "spese/fatture/sottocartella").mkdir()
    with index.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    for evidence in manifest["evidenze"]:
        if evidence["id"] == "indice-spese":
            evidence["sha256"] = hashlib.sha256(index.read_bytes()).hexdigest()
    result = module.valuta(manifest, tmp_path)
    assert result["verdetto"] == "BLOCCATO"
    assert "Prospetto spese: fattura duplicato alla riga 3" in "\n".join(result["blocchi"])


def test_numero_fattura_vuoto_blocca_la_coppia(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    index = tmp_path / manifest["spese"]["indice_csv"]
    rows = list(csv.DictReader(index.read_text(encoding="utf-8").splitlines()))
    rows[1]["numero_fattura"] = ""
    with index.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    for evidence in manifest["evidenze"]:
        if evidence["id"] == "indice-spese":
            evidence["sha256"] = hashlib.sha256(index.read_bytes()).hexdigest()
    result = module.valuta(manifest, tmp_path)
    assert result["verdetto"] == "BLOCCATO"
    assert "Prospetto spese: numero_fattura assente alla riga 3." in result["blocchi"]


def test_stessa_fattura_copiata_con_altro_nome_resta_un_duplicato(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    index = tmp_path / manifest["spese"]["indice_csv"]
    rows = list(csv.DictReader(index.read_text(encoding="utf-8").splitlines()))
    copied = tmp_path / "spese/fatture/fattura-1-copia.pdf"
    copied.write_bytes((tmp_path / rows[0]["fattura_path"]).read_bytes())
    rows[1]["fattura_path"] = str(copied.relative_to(tmp_path))
    rows[1]["fattura_sha256"] = rows[0]["fattura_sha256"]
    with index.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    for evidence in manifest["evidenze"]:
        if evidence["id"] == "indice-spese":
            evidence["sha256"] = hashlib.sha256(index.read_bytes()).hexdigest()

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "Prospetto spese: SHA-256 fattura duplicato alla riga 3." in result["blocchi"]


def test_chiave_fornitore_numero_data_blocca_la_stessa_fattura(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    index = tmp_path / manifest["spese"]["indice_csv"]
    rows = list(csv.DictReader(index.read_text(encoding="utf-8").splitlines()))
    rows[1]["fornitore_id"] = rows[0]["fornitore_id"]
    rows[1]["numero_fattura"] = rows[0]["numero_fattura"]
    rows[1]["data_fattura"] = rows[0]["data_fattura"]
    with index.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    for evidence in manifest["evidenze"]:
        if evidence["id"] == "indice-spese":
            evidence["sha256"] = hashlib.sha256(index.read_bytes()).hexdigest()

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "Prospetto spese: chiave fattura duplicata alla riga 3." in result["blocchi"]


def test_riferimento_pagamento_duplicato_blocca_il_doppio_conteggio(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    index = tmp_path / manifest["spese"]["indice_csv"]
    rows = list(csv.DictReader(index.read_text(encoding="utf-8").splitlines()))
    rows[1]["riferimento_pagamento"] = rows[0]["riferimento_pagamento"]
    with index.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    for evidence in manifest["evidenze"]:
        if evidence["id"] == "indice-spese":
            evidence["sha256"] = hashlib.sha256(index.read_bytes()).hexdigest()

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "Prospetto spese: riferimento_pagamento duplicato alla riga 3." in result["blocchi"]


def test_identificativi_spesa_unicode_equivalenti_restano_duplicati(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    index = tmp_path / manifest["spese"]["indice_csv"]
    rows = list(csv.DictReader(index.read_text(encoding="utf-8").splitlines()))
    rows[0]["fornitore_id"] = "ACME"
    rows[0]["numero_fattura"] = "F-1"
    rows[0]["riferimento_pagamento"] = "PAY-1"
    rows[1]["fornitore_id"] = "ＡＣＭＥ"
    rows[1]["numero_fattura"] = "Ｆ-１"
    rows[1]["data_fattura"] = rows[0]["data_fattura"]
    rows[1]["riferimento_pagamento"] = "ＰＡＹ-１"
    with index.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    for evidence in manifest["evidenze"]:
        if evidence["id"] == "indice-spese":
            evidence["sha256"] = hashlib.sha256(index.read_bytes()).hexdigest()

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "Prospetto spese: chiave fattura duplicata alla riga 3." in result["blocchi"]
    assert "Prospetto spese: riferimento_pagamento duplicato alla riga 3." in result["blocchi"]


def test_blocca_piu_di_un_gesto_umano_nella_stessa_fase(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    manifest["controlli"].append(
        {
            "id": "accesso",
            "voce": "Accesso al portale",
            "stato": "PASSAGGIO_UMANO",
            "evidenze": ["prova.pdf"],
            "azione": "",
            "categoria_umana": "accesso",
            "oggetto_evidenza": "prova.pdf",
        }
    )
    result = module.valuta(manifest, tmp_path)
    assert result["verdetto"] == "BLOCCATO"
    assert result["prossimo_passaggio_umano"] == ""
    assert "Piu di un gesto umano dichiarato nella stessa fase." in result["blocchi"]


def test_invio_non_emerge_dopo_la_firma_senza_validazione_digitale(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    manifest["controlli"][1] = {
        "id": "firma-titolare",
        "voce": "Firma del titolare applicata",
        "stato": "PROVATO",
        "evidenze": ["prova.pdf"],
        "azione": "",
    }
    manifest["pratica"]["fase"] = "invio"
    manifest["controlli"].append(
        {
            "id": "invio-finale",
            "voce": "Invio definitivo",
            "stato": "PASSAGGIO_UMANO",
            "evidenze": ["prova.pdf"],
            "azione": "",
            "categoria_umana": "invio-finale",
            "oggetto_evidenza": "prova.pdf",
        }
    )
    result = module.valuta(manifest, tmp_path)
    assert result["verdetto"] == "BLOCCATO"
    assert result["prossimo_passaggio_umano"] == ""
    assert "Validazione della firma digitale assente prima del pagamento o invio finale." in result["blocchi"]


def test_validazione_cades_provata_apre_il_solo_invio_finale(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    signed = evidence_file(tmp_path, "domanda.pdf.p7m", b"cades")
    receipt = evidence_file(tmp_path, "verifica-firma.txt", b"firma valida")
    manifest["evidenze"].extend([signed, receipt])
    manifest["pratica"]["fase"] = "invio"
    manifest["controlli"][1] = {
        "id": "firma-titolare",
        "voce": "Firma del titolare applicata",
        "stato": "PROVATO",
        "evidenze": [signed["id"]],
        "azione": "",
    }
    manifest["controlli"].extend(
        [
            {
                "id": "validazione-firma-digitale",
                "voce": "Firma CAdES valida e firmatario corretto",
                "stato": "PROVATO",
                "evidenze": ["prova.pdf", signed["id"], receipt["id"]],
                "azione": "",
            },
            {
                "id": "invio-finale",
                "voce": "Invio definitivo",
                "stato": "PASSAGGIO_UMANO",
                "evidenze": ["riepilogo-finale.pdf"],
                "azione": "",
                "categoria_umana": "invio-finale",
                "oggetto_evidenza": "riepilogo-finale.pdf",
            },
        ]
    )
    manifest["validazione_firma"] = {
        "richiesta": True,
        "formato": "CAdES",
        "firmatario_atteso": "Mario Rossi",
        "firmatario_verificato": "Mario Rossi",
        "originale_evidenza": "prova.pdf",
        "originale_sha256": manifest["evidenze"][0]["sha256"],
        "file_firmato_evidenza": signed["id"],
        "ricevuta_evidenza": receipt["id"],
        "strumento": "verificatore firma installato",
        "verificata_il": "2026-09-12T12:00:00+02:00",
        "esito": "VALIDA",
    }
    add_proven_payment(manifest, tmp_path)
    add_proven_summary(manifest)
    result = module.valuta(manifest, tmp_path)
    assert result["verdetto"] == "PRONTO"
    assert result["prossimo_passaggio_umano"] == (
        "Il titolare autorizza e compie l'invio finale del riepilogo `riepilogo-finale.pdf`."
    )


def test_invio_non_si_apre_senza_pagamento_provato_o_deroga_ufficiale(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    signed = evidence_file(tmp_path, "domanda.pdf.p7m", b"cades")
    receipt = evidence_file(tmp_path, "verifica-firma.txt", b"firma valida")
    manifest["evidenze"].extend([signed, receipt])
    manifest["pratica"]["fase"] = "invio"
    manifest["controlli"][1] = {
        "id": "firma-titolare",
        "voce": "Firma del titolare applicata",
        "stato": "PROVATO",
        "evidenze": [signed["id"]],
        "azione": "",
    }
    manifest["controlli"].extend(
        [
            {
                "id": "validazione-firma-digitale",
                "voce": "Firma CAdES valida e firmatario corretto",
                "stato": "PROVATO",
                "evidenze": [signed["id"], receipt["id"]],
                "azione": "",
            },
            {
                "id": "invio-finale",
                "voce": "Invio definitivo",
                "stato": "PASSAGGIO_UMANO",
                "evidenze": ["prova.pdf"],
                "azione": "",
                "categoria_umana": "invio-finale",
                "oggetto_evidenza": "prova.pdf",
            },
        ]
    )
    manifest["validazione_firma"] = {
        "richiesta": True,
        "formato": "CAdES",
        "firmatario_atteso": "Mario Rossi",
        "firmatario_verificato": "Mario Rossi",
        "file_firmato_evidenza": signed["id"],
        "ricevuta_evidenza": receipt["id"],
        "strumento": "verificatore firma installato",
        "verificata_il": "2026-09-12",
        "esito": "VALIDA",
    }

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "Pagamento non provato prima dell'invio finale." in result["blocchi"]


def test_gesto_pagamento_richiede_avviso_importo_e_riferimento_provati(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    add_valid_signature(manifest, tmp_path)
    manifest["pratica"]["fase"] = "pagamento"
    manifest["pagamento"] = {
        "richiesto": True,
        "avviso_evidenza": "prova.pdf",
    }
    manifest["controlli"].append(
        {
            "id": "pagamento",
            "voce": "Pagamento del bollo",
            "stato": "PASSAGGIO_UMANO",
            "evidenze": ["prova.pdf"],
            "azione": "",
            "categoria_umana": "pagamento",
            "oggetto_evidenza": "prova.pdf",
        }
    )

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert result["prossimo_passaggio_umano"] == ""
    assert "Avviso di pagamento incompleto prima del gesto del titolare." in result["blocchi"]


def test_avviso_pagamento_non_puo_essere_una_ricevuta_di_firma(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    add_valid_signature(manifest, tmp_path)
    signature_receipt_id = manifest["validazione_firma"]["ricevuta_evidenza"]
    signature_receipt = next(
        item for item in manifest["evidenze"] if item["id"] == signature_receipt_id
    )
    manifest["pratica"]["fase"] = "pagamento"
    manifest["pagamento"] = {
        "richiesto": True,
        "avviso_evidenza": signature_receipt_id,
        "avviso_sha256": signature_receipt["sha256"],
        "importo_atteso_eur": "16.00",
        "riferimento_atteso": "BOLLO-2026",
    }
    manifest["controlli"].extend(
        [
            {
                "id": "avviso-pagamento",
                "voce": "Avviso di pagamento verificato",
                "stato": "PROVATO",
                "evidenze": [signature_receipt_id],
                "azione": "",
            },
            {
                "id": "pagamento",
                "voce": "Pagamento del bollo",
                "stato": "PASSAGGIO_UMANO",
                "evidenze": [signature_receipt_id],
                "azione": "",
                "categoria_umana": "pagamento",
                "oggetto_evidenza": signature_receipt_id,
            },
        ]
    )

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "Avviso di pagamento sovrapposto a un altro artefatto della pratica." in result["blocchi"]


def test_deroga_pagamento_accetta_solo_la_fonte_ufficiale_esatta(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    official_id = manifest["fonti_ufficiali"][0]["evidenza_id"]
    manifest["pagamento"] = {
        "richiesto": False,
        "fonte_non_richiesto_evidenza": official_id,
    }
    control = {
        "id": "pagamento-non-richiesto",
        "voce": "La fonte ufficiale non richiede pagamento",
        "stato": "PROVATO",
        "evidenze": [official_id],
        "azione": "",
    }

    blocks = module._payment_blocks(
        manifest,
        "invio",
        {official_id},
        {official_id},
        {control["id"]: control},
    )

    assert blocks == []


def test_deroga_pagamento_non_accetta_una_nota_interna(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    internal = evidence_file(tmp_path, "nota-pagamento.txt", b"pagamento non richiesto")
    manifest["pagamento"] = {
        "richiesto": False,
        "fonte_non_richiesto_evidenza": internal["id"],
    }
    control = {
        "id": "pagamento-non-richiesto",
        "voce": "Una nota interna dice che il pagamento non serve",
        "stato": "PROVATO",
        "evidenze": [internal["id"]],
        "azione": "",
    }

    blocks = module._payment_blocks(
        manifest,
        "invio",
        {internal["id"]},
        set(),
        {control["id"]: control},
    )

    assert blocks == ["Pagamento dichiarato non richiesto senza prova sulla fonte ufficiale."]


def test_pagamento_rifiuta_timestamp_non_valido(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    add_proven_payment(manifest, tmp_path)
    manifest["pagamento"]["eseguito_il"] = "mai"
    receipt_id = manifest["pagamento"]["ricevuta_evidenza"]
    notice_id = manifest["pagamento"]["avviso_evidenza"]
    payment_control = next(
        control for control in manifest["controlli"] if control["id"] == "pagamento-completato"
    )

    blocks = module._payment_blocks(
        manifest,
        "invio",
        {notice_id, receipt_id},
        set(),
        proven_payment_controls(manifest),
    )

    assert blocks == ["Pagamento non provato prima dell'invio finale."]


def test_pagamento_completato_deve_corrispondere_all_avviso_originale(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    add_proven_payment(manifest, tmp_path)
    manifest["pagamento"]["importo_eur"] = "17.00"
    receipt_id = manifest["pagamento"]["ricevuta_evidenza"]
    notice_id = manifest["pagamento"]["avviso_evidenza"]
    payment_control = next(
        control for control in manifest["controlli"] if control["id"] == "pagamento-completato"
    )

    blocks = module._payment_blocks(
        manifest,
        "invio",
        {notice_id, receipt_id},
        set(),
        proven_payment_controls(manifest),
    )

    assert blocks == ["Pagamento completato non riferito all'avviso originale."]


def test_importi_pagamento_devono_essere_finiti_e_monetari(tmp_path: Path):
    module = load_module()
    for invalid_amount in ("Infinity", "NaN", "16.001"):
        case_root = tmp_path / invalid_amount.replace(".", "-")
        case_root.mkdir()
        manifest = base_manifest(case_root)
        add_proven_payment(manifest, case_root)
        manifest["pagamento"]["importo_atteso_eur"] = invalid_amount
        manifest["pagamento"]["importo_eur"] = invalid_amount
        notice_id = manifest["pagamento"]["avviso_evidenza"]
        receipt_id = manifest["pagamento"]["ricevuta_evidenza"]
        payment_control = next(
            control
            for control in manifest["controlli"]
            if control["id"] == "pagamento-completato"
        )

        blocks = module._payment_blocks(
            manifest,
            "invio",
            {notice_id, receipt_id},
            set(),
            proven_payment_controls(manifest),
        )

        assert blocks, invalid_amount


def test_avviso_non_puo_valere_anche_come_ricevuta_di_pagamento(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    add_proven_payment(manifest, tmp_path)
    notice_id = manifest["pagamento"]["avviso_evidenza"]
    manifest["pagamento"]["ricevuta_evidenza"] = notice_id
    payment_control = next(
        control for control in manifest["controlli"] if control["id"] == "pagamento-completato"
    )

    blocks = module._payment_blocks(
        manifest,
        "invio",
        {notice_id},
        set(),
        proven_payment_controls(manifest),
    )

    assert blocks == ["Avviso e ricevuta di pagamento devono essere evidenze distinte."]


def test_ricevute_di_firma_e_pagamento_non_possono_coincidere(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    add_valid_signature(manifest, tmp_path)
    add_proven_payment(manifest, tmp_path)
    signature_receipt_id = manifest["validazione_firma"]["ricevuta_evidenza"]
    notice_id = manifest["pagamento"]["avviso_evidenza"]
    manifest["pagamento"]["ricevuta_evidenza"] = signature_receipt_id
    payment_control = next(
        control for control in manifest["controlli"] if control["id"] == "pagamento-completato"
    )
    payment_control["evidenze"] = [notice_id, signature_receipt_id]
    manifest["pratica"]["fase"] = "invio"
    manifest["controlli"].append(
        {
            "id": "invio-finale",
            "voce": "Invio definitivo",
            "stato": "PASSAGGIO_UMANO",
            "evidenze": ["prova.pdf"],
            "azione": "",
            "categoria_umana": "invio-finale",
            "oggetto_evidenza": "prova.pdf",
        }
    )

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "Le ricevute di firma, pagamento e protocollo devono essere distinte." in result["blocchi"]


def test_file_firmato_non_puo_valere_come_ricevuta_di_pagamento(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    add_valid_signature(manifest, tmp_path)
    add_proven_payment(manifest, tmp_path)
    signed_id = manifest["validazione_firma"]["file_firmato_evidenza"]
    notice_id = manifest["pagamento"]["avviso_evidenza"]
    manifest["pagamento"]["ricevuta_evidenza"] = signed_id
    payment_control = next(
        control for control in manifest["controlli"] if control["id"] == "pagamento-completato"
    )
    payment_control["evidenze"] = [notice_id, signed_id]
    manifest["pratica"]["fase"] = "invio"
    add_proven_summary(manifest)
    summary_id = manifest["output_finale"]["riepilogo_invio_evidenza"]
    manifest["controlli"].append(
        {
            "id": "invio-finale",
            "voce": "Invio definitivo",
            "stato": "PASSAGGIO_UMANO",
            "evidenze": [summary_id],
            "azione": "",
            "categoria_umana": "invio-finale",
            "oggetto_evidenza": summary_id,
        }
    )

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "Gli artefatti critici della pratica devono avere ruoli distinti." in result["blocchi"]


def test_fase_presentata_richiede_ricevuta_o_protocollo_provato(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    manifest["pratica"]["fase"] = "presentata"
    result = module.valuta(manifest, tmp_path)
    assert result["verdetto"] == "BLOCCATO"
    assert "Fase PRESENTATA senza ricevuta o protocollo finale provato." in result["blocchi"]


def test_presentata_non_passa_se_firma_o_invio_sono_ancora_pendenti(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    receipt = evidence_file(tmp_path, "ricevuta-protocollo.pdf", b"protocollo finale")
    manifest["evidenze"].append(receipt)
    manifest["pratica"]["fase"] = "presentata"
    manifest["controlli"].append(
        {
            "id": "ricevuta-protocollo",
            "voce": "Ricevuta finale",
            "stato": "PROVATO",
            "evidenze": [receipt["id"]],
            "azione": "",
        }
    )
    manifest["presentazione"] = {
        "ricevuta_evidenza": receipt["id"],
        "numero_protocollo": "GE-2026-123",
        "presentata_il": "2026-09-14T14:01:00+02:00",
        "portale": "ReStart",
    }

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert result["fase_confermata"] == ""
    assert "Fase PRESENTATA con gesti umani ancora pendenti." in result["blocchi"]


def test_presentata_richiede_metadati_e_ricevuta_esatta(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    manifest["controlli"] = [manifest["controlli"][0]]
    manifest["pratica"]["fase"] = "presentata"
    manifest["controlli"].append(
        {
            "id": "ricevuta-protocollo",
            "voce": "Ricevuta finale",
            "stato": "PROVATO",
            "evidenze": ["prova.pdf"],
            "azione": "",
        }
    )

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert result["fase_confermata"] == ""
    assert "Fase PRESENTATA senza metadati completi della presentazione finale." in result["blocchi"]


def test_presentata_non_aggira_la_validazione_della_firma_richiesta(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    receipt = evidence_file(tmp_path, "ricevuta-protocollo.pdf", b"protocollo finale")
    manifest["evidenze"].append(receipt)
    manifest["controlli"] = [manifest["controlli"][0]]
    manifest["controlli"].append(
        {
            "id": "ricevuta-protocollo",
            "voce": "Ricevuta finale",
            "stato": "PROVATO",
            "evidenze": [receipt["id"]],
            "azione": "",
        }
    )
    manifest["pratica"]["fase"] = "presentata"
    manifest["validazione_firma"] = {"richiesta": True}
    manifest["presentazione"] = {
        "ricevuta_evidenza": receipt["id"],
        "numero_protocollo": "GE-2026-123",
        "presentata_il": "2026-09-14T14:01:00+02:00",
        "portale": "ReStart",
    }

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert result["fase_confermata"] == ""
    assert "Validazione della firma digitale assente prima del pagamento o invio finale." in result["blocchi"]


def test_presentata_non_puo_autodichiarare_che_la_firma_non_serve(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    receipt = evidence_file(tmp_path, "ricevuta-protocollo.pdf", b"protocollo finale")
    manifest["evidenze"].append(receipt)
    manifest["controlli"] = [manifest["controlli"][0]]
    manifest["controlli"].append(
        {
            "id": "ricevuta-protocollo",
            "voce": "Ricevuta finale",
            "stato": "PROVATO",
            "evidenze": [receipt["id"]],
            "azione": "",
        }
    )
    manifest["pratica"]["fase"] = "presentata"
    manifest["validazione_firma"] = {"richiesta": False}
    manifest["presentazione"] = {
        "ricevuta_evidenza": receipt["id"],
        "numero_protocollo": "GE-2026-123",
        "presentata_il": "2026-09-14T14:01:00+02:00",
        "portale": "ReStart",
    }

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert result["fase_confermata"] == ""
    assert "Firma dichiarata non richiesta senza prova sulla fonte ufficiale." in result["blocchi"]


def test_deroga_firma_non_accetta_un_file_interno_come_fonte_ufficiale(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    internal = evidence_file(tmp_path, "nota-interna.pdf", b"nota interna")
    receipt = evidence_file(tmp_path, "ricevuta-protocollo.pdf", b"protocollo finale")
    manifest["evidenze"].extend([internal, receipt])
    manifest["controlli"] = [manifest["controlli"][0]]
    manifest["controlli"].extend(
        [
            {
                "id": "firma-non-richiesta",
                "voce": "La fonte ufficiale non richiede firma",
                "stato": "PROVATO",
                "evidenze": [internal["id"]],
                "azione": "",
            },
            {
                "id": "ricevuta-protocollo",
                "voce": "Ricevuta finale",
                "stato": "PROVATO",
                "evidenze": [receipt["id"]],
                "azione": "",
            },
        ]
    )
    manifest["pratica"]["fase"] = "presentata"
    manifest["validazione_firma"] = {
        "richiesta": False,
        "fonte_non_richiesta_evidenza": internal["id"],
    }
    manifest["presentazione"] = {
        "ricevuta_evidenza": receipt["id"],
        "numero_protocollo": "GE-2026-123",
        "presentata_il": "2026-09-14T14:01:00+02:00",
        "portale": "ReStart",
    }

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "Firma dichiarata non richiesta senza prova sulla fonte ufficiale." in result["blocchi"]


def test_presentata_con_firma_validata_e_protocollo_viene_confermata(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    signed = evidence_file(tmp_path, "domanda.pdf.p7m", b"cades")
    validation = evidence_file(tmp_path, "verifica-firma.txt", b"firma valida")
    receipt = evidence_file(tmp_path, "ricevuta-protocollo.pdf", b"protocollo finale")
    manifest["evidenze"].extend([signed, validation, receipt])
    manifest["controlli"] = [manifest["controlli"][0], manifest["controlli"][2]]
    manifest["controlli"].extend(
        [
            {
                "id": "firma-titolare",
                "voce": "Firma del titolare applicata",
                "stato": "PROVATO",
                "evidenze": [signed["id"]],
                "azione": "",
            },
            {
                "id": "validazione-firma-digitale",
                "voce": "Firma CAdES valida e firmatario corretto",
                "stato": "PROVATO",
                "evidenze": ["prova.pdf", signed["id"], validation["id"]],
                "azione": "",
            },
            {
                "id": "ricevuta-protocollo",
                "voce": "Ricevuta finale",
                "stato": "PROVATO",
                "evidenze": ["riepilogo-finale.pdf", receipt["id"]],
                "azione": "",
            },
        ]
    )
    manifest["validazione_firma"] = {
        "richiesta": True,
        "formato": "CAdES",
        "firmatario_atteso": "Mario Rossi",
        "firmatario_verificato": "Mario Rossi",
        "originale_evidenza": "prova.pdf",
        "originale_sha256": manifest["evidenze"][0]["sha256"],
        "file_firmato_evidenza": signed["id"],
        "ricevuta_evidenza": validation["id"],
        "strumento": "verificatore firma installato",
        "verificata_il": "2026-09-12T12:00:00+02:00",
        "esito": "VALIDA",
    }
    manifest["pratica"]["fase"] = "presentata"
    manifest["presentazione"] = {
        "riepilogo_evidenza": "riepilogo-finale.pdf",
        "riepilogo_sha256": manifest["evidenze"][2]["sha256"],
        "ricevuta_evidenza": receipt["id"],
        "pratica_id_atteso": "DOMANDA-2026-123",
        "pratica_id_ricevuta": "DOMANDA-2026-123",
        "numero_protocollo": "GE-2026-123",
        "presentata_il": "2026-09-12T12:20:00+02:00",
        "portale": "ReStart",
    }
    add_proven_payment(manifest, tmp_path)
    add_proven_summary(manifest)

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "PRONTO"
    assert result["fase_confermata"] == "PRESENTATA"


def test_ricevuta_finale_deve_riferirsi_al_riepilogo_inviato(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    add_valid_signature(manifest, tmp_path)
    add_proven_payment(manifest, tmp_path)
    receipt = evidence_file(tmp_path, "ricevuta-altra-pratica.pdf", b"protocollo pratica B")
    manifest["evidenze"].append(receipt)
    manifest["controlli"].append(
        {
            "id": "ricevuta-protocollo",
            "voce": "Ricevuta finale",
            "stato": "PROVATO",
            "evidenze": [receipt["id"]],
            "azione": "",
        }
    )
    manifest["pratica"]["fase"] = "presentata"
    manifest["presentazione"] = {
        "riepilogo_evidenza": "prova.pdf",
        "riepilogo_sha256": manifest["evidenze"][0]["sha256"],
        "ricevuta_evidenza": receipt["id"],
        "pratica_id_atteso": "DOMANDA-A",
        "pratica_id_ricevuta": "DOMANDA-B",
        "numero_protocollo": "GE-2026-B",
        "presentata_il": "2026-09-12T12:20:00+02:00",
        "portale": "ReStart",
    }

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert result["fase_confermata"] == ""
    assert "Ricevuta finale non riferita al riepilogo inviato." in result["blocchi"]


def test_riepilogo_inviato_non_puo_valere_come_ricevuta_finale(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    add_valid_signature(manifest, tmp_path)
    add_proven_payment(manifest, tmp_path)
    summary_id = manifest["output_finale"]["riepilogo_invio_evidenza"]
    summary = next(item for item in manifest["evidenze"] if item["id"] == summary_id)
    manifest["controlli"].append(
        {
            "id": "ricevuta-protocollo",
            "voce": "Ricevuta finale",
            "stato": "PROVATO",
            "evidenze": [summary_id],
            "azione": "",
        }
    )
    manifest["pratica"]["fase"] = "presentata"
    manifest["presentazione"] = {
        "riepilogo_evidenza": summary_id,
        "riepilogo_sha256": summary["sha256"],
        "ricevuta_evidenza": summary_id,
        "pratica_id_atteso": "DOMANDA-A",
        "pratica_id_ricevuta": "DOMANDA-A",
        "numero_protocollo": "GE-2026-A",
        "presentata_il": "2026-09-12T12:20:00+02:00",
        "portale": "ReStart",
    }

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert "Riepilogo inviato e ricevuta finale devono essere evidenze distinte." in result["blocchi"]


def test_presentata_blocca_una_cronologia_impossibile(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    add_valid_signature(manifest, tmp_path)
    add_proven_payment(manifest, tmp_path)
    receipt = evidence_file(tmp_path, "ricevuta-protocollo.pdf", b"protocollo finale")
    manifest["evidenze"].append(receipt)
    manifest["controlli"].append(
        {
            "id": "ricevuta-protocollo",
            "voce": "Ricevuta finale",
            "stato": "PROVATO",
            "evidenze": [receipt["id"]],
            "azione": "",
        }
    )
    manifest["pratica"]["fase"] = "presentata"
    manifest["validazione_firma"]["verificata_il"] = "2026-09-12T12:20:00+02:00"
    manifest["pagamento"]["eseguito_il"] = "2026-09-12T12:30:00+02:00"
    manifest["presentazione"] = {
        "ricevuta_evidenza": receipt["id"],
        "numero_protocollo": "GE-2026-125",
        "presentata_il": "2026-09-12T12:10:00+02:00",
        "portale": "ReStart",
    }

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert result["fase_confermata"] == ""
    assert "Cronologia impossibile tra firma, pagamento e presentazione." in result["blocchi"]


def test_presentata_blocca_timestamp_futuri_anche_se_ordinati(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    add_valid_signature(manifest, tmp_path)
    add_proven_payment(manifest, tmp_path)
    receipt = evidence_file(tmp_path, "ricevuta-protocollo.pdf", b"protocollo finale")
    manifest["evidenze"].append(receipt)
    manifest["controlli"].append(
        {
            "id": "ricevuta-protocollo",
            "voce": "Ricevuta finale",
            "stato": "PROVATO",
            "evidenze": [receipt["id"]],
            "azione": "",
        }
    )
    manifest["pratica"]["fase"] = "presentata"
    manifest["validazione_firma"]["verificata_il"] = "2099-01-01T10:00:00+01:00"
    manifest["pagamento"]["eseguito_il"] = "2099-01-01T10:01:00+01:00"
    manifest["presentazione"] = {
        "ricevuta_evidenza": receipt["id"],
        "numero_protocollo": "GE-2099-001",
        "presentata_il": "2099-01-01T10:02:00+01:00",
        "portale": "ReStart",
    }

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "BLOCCATO"
    assert result["fase_confermata"] == ""
    assert "Cronologia futura impossibile per una fase dichiarata completata." in result["blocchi"]


def test_presentata_senza_firma_passa_solo_con_deroga_ufficiale_provata(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    receipt = evidence_file(tmp_path, "ricevuta-protocollo.pdf", b"protocollo finale")
    manifest["evidenze"].append(receipt)
    official_id = manifest["fonti_ufficiali"][0]["evidenza_id"]
    manifest["controlli"] = [manifest["controlli"][0]]
    manifest["controlli"].extend(
        [
            {
                "id": "firma-non-richiesta",
                "voce": "La fonte ufficiale non richiede firma",
                "stato": "PROVATO",
                "evidenze": [official_id],
                "azione": "",
            },
            {
                "id": "ricevuta-protocollo",
                "voce": "Ricevuta finale",
                "stato": "PROVATO",
                "evidenze": ["riepilogo-finale.pdf", receipt["id"]],
                "azione": "",
            },
        ]
    )
    manifest["validazione_firma"] = {
        "richiesta": False,
        "fonte_non_richiesta_evidenza": official_id,
    }
    manifest["pratica"]["fase"] = "presentata"
    manifest["presentazione"] = {
        "riepilogo_evidenza": "riepilogo-finale.pdf",
        "riepilogo_sha256": manifest["evidenze"][2]["sha256"],
        "ricevuta_evidenza": receipt["id"],
        "pratica_id_atteso": "DOMANDA-2026-124",
        "pratica_id_ricevuta": "DOMANDA-2026-124",
        "numero_protocollo": "GE-2026-124",
        "presentata_il": "2026-09-12T12:20:00+02:00",
        "portale": "ReStart",
    }
    add_proven_payment(manifest, tmp_path)
    add_proven_summary(manifest)

    result = module.valuta(manifest, tmp_path)

    assert result["verdetto"] == "PRONTO"
    assert result["fase_confermata"] == "PRESENTATA"


def test_coppia_integra_con_ammissibilita_esterna_pendente_da_in_attesa(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    manifest["controlli"].append(
        {
            "id": "data-ammissibilita",
            "voce": "Data iniziale delle spese",
            "stato": "IN_ATTESA_ESTERNA",
            "evidenze": [],
            "azione": "Attendere la risposta scritta dell'ente sulla data iniziale.",
        }
    )
    index = tmp_path / manifest["spese"]["indice_csv"]
    rows = list(csv.DictReader(index.read_text(encoding="utf-8").splitlines()))
    rows[1]["stato"] = "IN_ATTESA"
    rows[1]["attesa_controllo_id"] = "data-ammissibilita"
    with index.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    for evidence in manifest["evidenze"]:
        if evidence["id"] == "indice-spese":
            evidence["sha256"] = hashlib.sha256(index.read_bytes()).hexdigest()
    manifest["spese"]["totale_ammesso_eur"] = "40.00"
    result = module.valuta(manifest, tmp_path)
    assert result["verdetto"] == "IN ATTESA"
    assert result["blocchi"] == []
    assert result["attese_esterne"] == ["Attendere la risposta scritta dell'ente sulla data iniziale."]


def test_indice_csv_deve_essere_l_evidenza_hashata_delle_spese(tmp_path: Path):
    module = load_module()
    manifest = base_manifest(tmp_path)
    manifest["evidenze"] = [
        evidence for evidence in manifest["evidenze"] if evidence["id"] != "indice-spese"
    ]
    manifest["spese"]["evidenze"] = ["prova.pdf"]
    result = module.valuta(manifest, tmp_path)
    assert result["verdetto"] == "BLOCCATO"
    assert "Il prospetto indicato da indice_csv non coincide con un'evidenza integra delle spese." in result["blocchi"]


def test_cli_scrive_report_e_ricevuta_legati_al_manifest(tmp_path: Path):
    manifest = base_manifest(tmp_path)
    manifest_path = tmp_path / "controllo.json"
    report_path = tmp_path / "REPORT.md"
    receipt_path = tmp_path / "RICEVUTA.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            str(manifest_path),
            "--root",
            str(tmp_path),
            "--report",
            str(report_path),
            "--ricevuta",
            str(receipt_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert completed.stdout.strip() == "ISPETTORE_BANDO_OK: PRONTO"
    assert report_path.read_text(encoding="utf-8").startswith("# Ispettore del Bando\n\n**Verdetto: PRONTO**")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["esito"] == "ISPETTORE_BANDO_OK"
    assert receipt["verdetto"] == "PRONTO"
    assert receipt["manifest_sha256"] == hashlib.sha256(manifest_path.read_bytes()).hexdigest()
