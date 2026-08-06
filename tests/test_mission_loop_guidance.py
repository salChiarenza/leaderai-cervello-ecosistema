import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class MissionLoopGuidanceTest(unittest.TestCase):
    def test_checkup_contains_closed_mission_loop(self):
        text = (ROOT / "CHECKUP.md").read_text(encoding="utf-8")

        required = [
            "Protocollo missione chiusa",
            "MISSIONE",
            "ESECUZIONE",
            "AUTOCONTROLLO",
            "SALVATAGGIO NELLA CASA",
            "CHIUSURA LOCALE",
            "attiva un autocontrollo",
            "aggiornamenti di avanzamento",
            "archivia l'email della missione",
            "DA DECIDERE IN CALL",
            "BLOCCO REALE",
            "una domanda unica",
            "riprendi la stessa missione",
            "Perfetto, l'ho fatto. Tutto completato e funzionante.",
            "una volta sola",
            "soltanto con esito `PASSA`",
        ]

        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_client_template_contains_closed_mission_loop(self):
        text = " ".join(
            (ROOT / "templates" / "AGENTS.md").read_text(encoding="utf-8").split()
        )
        processes = (ROOT / "templates" / "PROCESSI.md").read_text(encoding="utf-8")

        required = [
            "Missioni da LeaderAI",
            "Il protocollo completo vive in `ecosistema/PROCESSI.md`",
            "AUTOCONTROLLO",
            "SALVATAGGIO NELLA CASA",
            "CHIUSURA LOCALE",
            "aggiornamenti di avanzamento",
            "Archivia nello stesso giro",
            "DA DECIDERE IN CALL",
            "BLOCCO REALE",
            "una domanda unica",
            "riprende la stessa missione",
            "Perfetto, l'ho fatto. Tutto completato e funzionante.",
            "una volta sola",
            "soltanto con esito `PASSA`",
        ]

        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

        self.assertIn("Protocollo missioni LeaderAI", processes)
        self.assertIn("MISSIONE -> ESECUZIONE -> AUTOCONTROLLO", processes)

    def test_delivery_contract_enforces_single_real_blocker(self):
        email = " ".join(
            (ROOT / "EMAIL_CONSEGNA.md").read_text(encoding="utf-8").split()
        )
        manifest = " ".join(
            (ROOT / "MANIFEST.md").read_text(encoding="utf-8").split()
        )

        for phrase in [
            "BLOCCO REALE",
            "Ho gia' provato",
            "Mi manca",
            "Domanda unica: Come proseguo su questo punto?",
            "Dopo la risposta riprendi la stessa missione",
            "Perfetto, l'ho fatto. Tutto completato e funzionante.",
        ]:
            with self.subTest(source="email", phrase=phrase):
                self.assertIn(phrase, email)

        for phrase in [
            "Legge dell'unico blocco reale",
            "una domanda unica",
            "riprende la stessa missione",
            "Aggiornamenti di avanzamento e domande a puntate sono vietati",
            "Perfetto, l'ho fatto. Tutto completato e funzionante.",
        ]:
            with self.subTest(source="manifest", phrase=phrase):
                self.assertIn(phrase, manifest)


if __name__ == "__main__":
    unittest.main()
