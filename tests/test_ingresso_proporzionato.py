import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAPPA = ROOT / "templates" / "AGENTS.md"
CHECKUP = ROOT / "CHECKUP.md"


def _flat(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


class IngressoProporzionatoTest(unittest.TestCase):
    """Miglioramento portato da Sal il 17/09/2026, provato prima nella sua casa.

    La mappa del cliente ordinava di leggere a ogni avvio la mappa, la memoria
    e **tutta** la chat degli assistenti: anche per «qual e' la mia partita
    IVA?». L'ingresso si paga a ogni domanda. Ora l'apertura e' proporzionata
    alla richiesta: dato gia' mappato = sola fonte proprietaria; lavoro
    operativo, modifica o coordinamento = stato, chat e mappa della stanza.
    """

    def test_a_simple_question_opens_only_the_owning_source(self):
        testo = _flat(MAPPA)
        self.assertIn("Domanda puntuale su un dato gia' mappato", testo)
        self.assertIn("apri soltanto la fonte che possiede quel dato", testo)

    def test_operational_work_opens_state_chat_and_room_map(self):
        testo = _flat(MAPPA)
        self.assertIn("Lavoro operativo, modifica o coordinamento", testo)
        for fonte in ("stato corrente", "AGENT_CHAT.md", "mappa della stanza"):
            with self.subTest(fonte=fonte):
                self.assertIn(fonte, testo)

    def test_the_map_no_longer_orders_the_whole_chat_at_every_start(self):
        testo = _flat(MAPPA)
        self.assertNotIn("All'avvio leggi nell'ordine", testo)
        self.assertNotIn("e tutto `AGENT_CHAT.md`", testo)

    def test_an_unchanged_source_is_not_read_twice(self):
        self.assertIn(
            "non rileggere una fonte che non e' cambiata", _flat(MAPPA).lower()
        )

    def test_the_rule_stays_generic(self):
        """Niente percorsi o nomi della casa di Sal dentro il prodotto."""
        testo = MAPPA.read_text(encoding="utf-8")
        for specifico in ("/Users/sal", "docs/STATUS.md", "docs/AGENT_CHAT.md", "leaderai/"):
            with self.subTest(specifico=specifico):
                self.assertNotIn(specifico, testo)

    def test_the_checkup_verifies_the_rule_on_existing_houses(self):
        testo = _flat(CHECKUP)
        self.assertIn("ingresso proporzionato", testo.lower())
        self.assertIn("Domanda puntuale", testo)


if __name__ == "__main__":
    unittest.main()
