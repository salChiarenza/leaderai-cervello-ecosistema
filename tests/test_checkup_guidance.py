import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CheckupGuidanceTest(unittest.TestCase):
    def test_inspector_compares_live_official_sources_and_does_not_double_ask(self):
        checkup = (ROOT / "CHECKUP.md").read_text(encoding="utf-8")
        checkup_normalized = " ".join(checkup.lower().split())
        skill = (ROOT / "templates" / "ISPETTORE_SKILL.md").read_text(
            encoding="utf-8"
        )
        agents = (ROOT / "templates" / "AGENTS.md").read_text(encoding="utf-8")
        required = [
            "install_contract.json -> official_sources",
            "https://code.claude.com/docs/en/overview",
            "https://learn.chatgpt.com/docs",
            "https://openai.com/it-IT/academy/codex-for-work/",
            "fonte -> regola ufficiale -> stato osservato -> scostamento",
            "FONTI UFFICIALI CONFRONTATE",
            "non puo' sostituire una specifica tecnica",
            "NON PASSA",
        ]
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(" ".join(phrase.lower().split()), checkup_normalized)

        self.assertIn("Non chiedere di nuovo se vuole avviarlo", skill)
        self.assertIn("non chiedere una\nseconda volta se partire", agents)

    def test_checkup_is_name_agnostic_and_uses_life_signals(self):
        text = (ROOT / "CHECKUP.md").read_text(encoding="utf-8")

        required = [
            "Il nome non basta",
            "puo' chiamarsi in qualunque modo",
            "segnali di vita",
            "memory/MEMORY.md compilata",
            "logs/ con attivita'",
            "logs/ con attivita'",
            "ecosistema/ASSET.md",
            "commit git",
            "file di lavoro recenti",
            "connettori provati",
        ]

        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_checkup_forces_extended_search_for_suspicious_leaderai_folders(self):
        text = (ROOT / "CHECKUP.md").read_text(encoding="utf-8")

        required = [
            "ricerca estesa obbligatoria",
            "LeaderAI",
            "Leader AI",
            "leader ai",
            "leder ai",
            "_leaderai",
            "leaderai-cervello-ecosistema",
            "Downloads",
            "OneDrive",
            "PowerShell",
            "SOSPETTA",
            "nessuna cartella sospetta",
        ]

        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_checkup_audits_room_graph_and_routes(self):
        text = (ROOT / "CHECKUP.md").read_text(encoding="utf-8")

        required = [
            "Censimento e rete delle stanze",
            "STANZA",
            "CAPACITA",
            "collegamenti a monte e collegamenti a valle",
            "ogni stanza sia raggiungibile",
            "PROPOSTA STRUTTURALE",
            "richiesta -> madre/stanza -> fonte -> capacita'/processo -> output",
            "LEZIONE CANDIDATA",
            "VERSIONE METODO",
            "Ispettore Ecosistema",
            "cartella visibile non classificata",
            "templates/STANZA_AGENTS.md",
            "templates/STANZA_FONTE.md",
            "percorso | classe | responsabilita business | amministratore | riporta al",
            "cartelle generiche",
            "file sciolto nella home",
            "il gate e' `NON PASSA`",
            "autoMemoryDirectory",
            "due memorie divergenti",
            "REPORT_FINALE.md` e' un residuo legacy",
            "fonte modificabile vive fuori dal codice",
            "non aprirle",
            "indice/history Git",
            "Firma, timbro e sigillo",
            "stato corrente",
            "prossimo passo",
            "scadenze",
            "Non creare una cartella\n`istituzionali/`",
            "responsabilita' business",
            "`Portafoglio Modello`",
            "pipeline tecnica, non una stanza",
        ]
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), text.lower())

    def test_checkup_measures_markdown_and_promotes_daily_lessons(self):
        checkup = (ROOT / "CHECKUP.md").read_text(encoding="utf-8")
        skill = (ROOT / "templates" / "ISPETTORE_SKILL.md").read_text(
            encoding="utf-8"
        )
        manifest = (ROOT / "MANIFEST.md").read_text(encoding="utf-8")
        combined = " ".join((checkup + skill + manifest).lower().split())
        required = [
            "inspection_policies -> markdown_hygiene",
            "AGENTS.md`, `MEMORY.md` e `AGENT_CHAT.md",
            "350 righe o 24 KiB",
            "800 righe o 80 KiB",
            "senza creare copie parallele",
            "caso, causa, riparazione",
            "diventa un controllo dei checkup successivi",
        ]
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(" ".join(phrase.lower().split()), combined)

        checkup = (ROOT / "CHECKUP.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(checkup.count("templates/STANZA_FONTE.md"), 6)
        mission = checkup.split("## Modello email missione checkup", 1)[1].split(
            "## ", 1
        )[0]
        self.assertIn("templates/STANZA_FONTE.md", mission)
        proof = checkup.split("STANDARD APPLICATO:", 1)[1]
        self.assertIn("templates/STANZA_FONTE.md", proof)

    def test_checkup_enforces_boss_and_sector_administrators(self):
        checkup = (ROOT / "CHECKUP.md").read_text(encoding="utf-8")
        root_map = (ROOT / "templates" / "AGENTS.md").read_text(encoding="utf-8")
        room_map = (ROOT / "templates" / "STANZA_AGENTS.md").read_text(
            encoding="utf-8"
        )
        skill = (ROOT / "templates" / "ISPETTORE_SKILL.md").read_text(
            encoding="utf-8"
        )
        combined = " ".join(
            (checkup + root_map + room_map + skill).lower().split()
        )
        required = [
            "Boss dell'Ecosistema",
            "Amministratore di settore",
            "ogni ramo organizzativo",
            "nuovo o preesistente",
            "riporta al Boss",
            "governa l'organigramma",
            "amministratore | riporta al",
        ]
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(" ".join(phrase.lower().split()), combined)

    def test_room_prefab_and_common_registry_are_enforced_everywhere(self):
        surfaces = [
            ROOT / "MANIFEST.md",
            ROOT / "CHECKUP.md",
            ROOT / "INSTALLA_CON_AI.md",
            ROOT / "templates" / "AGENTS.md",
            ROOT / "templates" / "ISPETTORE_SKILL.md",
        ]
        combined = " ".join(
            " ".join(path.read_text(encoding="utf-8").lower().split())
            for path in surfaces
        )
        required = [
            "ecosistema/` e' l'armadio comune",
            "ecosistema/stanza_fonte.md",
            "inspection_policies -> room_lifecycle",
            "sottocartella diretta",
            "fonte operativa",
            "stesso salvataggio",
        ]
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(" ".join(phrase.lower().split()), combined)

    def test_checkup_blocks_circular_operational_evidence(self):
        text = (ROOT / "CHECKUP.md").read_text(encoding="utf-8")

        required = [
            "Gate anti-collaudo circolare",
            "email della missione",
            "richiesta inventata",
            "creato soltanto per far passare il checkup",
            "usati nel lavoro quotidiano",
            "esisteva prima del checkup",
            "PROVENIENZA PROVE",
            "GATE ANTI-CIRCOLARE",
            "NON PASSA",
        ]
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), text.lower())

    def test_checkup_measures_observed_adoption_with_period_and_dedup(self):
        checkup = " ".join(
            (ROOT / "CHECKUP.md").read_text(encoding="utf-8").lower().split()
        )

        required = [
            "Come si lavora davvero qui dentro",
            "NON USATO NEL PERIODO OSSERVATO",
            "OSSERVAZIONE PARZIALE - UNA POSTAZIONE",
            "TRACCE ASSENTI",
            "mai un giudizio di mancato uso",
            "stesso episodio presente in Git, chat e diario vale uno",
            "adoption_rule.py -> classify_adoption",
            "inspection_policies -> adoption_observation",
            "da quale macchina",
            "sola presenza di un file non basta",
            "gesto manuale esplicito",
            "VERDETTO CONFORMITA'",
            "ADOZIONE OSSERVATA",
            "misura della spesa e del consumo appartiene al prodotto",
            "Il Consigliere",
        ]
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(" ".join(phrase.lower().split()), checkup)

    def test_instruction_audit_uses_clean_pairwise_sessions_and_safe_classification(self):
        checkup = (ROOT / "CHECKUP.md").read_text(encoding="utf-8")
        skill = (ROOT / "templates" / "ISPETTORE_SKILL.md").read_text(
            encoding="utf-8"
        )
        combined = " ".join((checkup + skill).split())
        required = [
            "Audit delle istruzioni che stringono troppo",
            "una istruzione o un gruppo coerente",
            "due task/sessioni nuove",
            "senza suggerire cartella, fonte, procedura o risultato atteso",
            "esito osservabile",
            "fonti corrette",
            "instradamento",
            "richieste/correzioni umane",
            "consumo quando esposto",
            "behavior_harness.py compare-context",
            "MANTIENI",
            "ACCORPA",
            "SPOSTA NELLA PROCEDURA/SKILL GIUSTA",
            "RISCRIVI",
            "CANDIDATA ALLA RIMOZIONE",
            "Sicurezza, privacy, autorizzazione e integrita'",
            "nessuna modifica distruttiva",
            "Un solo caso non puo'",
        ]
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(" ".join(phrase.split()), combined)

    def test_instruction_audit_contract_contains_the_anonymous_regressions(self):
        import json

        contract = json.loads((ROOT / "install_contract.json").read_text(encoding="utf-8"))
        policy = contract["inspection_policies"]["instruction_audit"]
        self.assertEqual(len(policy["classifications"]), 5)
        self.assertEqual(
            set(policy["protected_semantics"]),
            {"safety", "privacy", "authorization", "integrity"},
        )
        self.assertEqual(
            set(policy["initial_cases"]),
            {
                "unverified_source",
                "wrong_owner_route",
                "duplicate_or_stale_source",
                "excess_rules_or_files",
                "conflicting_instructions",
                "missing_final_verification",
                "unnecessary_human_request",
            },
        )


if __name__ == "__main__":
    unittest.main()
