"""Regola di Sal del 18/09/2026: nella casa del cliente niente si lancia a mano.

Tre difetti visti nella casa di una cliente lo stesso giorno:
- la manutenzione vedeva la mappa al limite e lasciava il lavoro a lei;
- due attivita' nate per un giro solo restavano nella sua lista, morte;
- nessuna pagina diceva cosa fosse acceso e come si spegne.
"""
from __future__ import annotations

import unittest
from pathlib import Path

PRODOTTO = Path(__file__).resolve().parents[1]
TEMPLATES = PRODOTTO / "templates"


def leggi(nome: str) -> str:
    return (TEMPLATES / nome).read_text(encoding="utf-8")


class CapacitaAutomaticheTest(unittest.TestCase):
    def test_il_manutentore_accorpa_la_mappa_al_tetto(self):
        testo = leggi("MANUTENTORE_SKILL.md")
        self.assertIn("Mappa arrivata al tetto", testo)
        self.assertIn("la accorpi tu nello stesso giro", testo)
        self.assertIn("quanto era grande prima", testo)

    def test_le_routine_di_un_giro_solo_si_tolgono(self):
        manutentore = leggi("MANUTENTORE_SKILL.md")
        ispettore = leggi("ISPETTORE_SKILL.md")
        for testo in (manutentore, ispettore):
            self.assertIn("usa e getta", testo)
        self.assertIn("Chi apre una routine la chiude", ispettore)
        self.assertIn("Routine che hanno finito", manutentore)

    def test_la_pagina_di_cosa_e_acceso_esiste_ed_e_per_il_proprietario(self):
        pagina = leggi("COSA_E_ACCESO.md")
        for riga in ("Quando parte", "Come si spegne", "Dove scrive"):
            self.assertIn(riga, pagina)
        self.assertIn("GUARDIANI.md", pagina)          # un solo elenco, non due
        self.assertNotIn(".agent/hooks", pagina)       # niente percorsi tecnici
        self.assertIn("COSA_E_ACCESO.md", leggi("MANUTENTORE_SKILL.md"))


class PonteManutenzioneControlloTest(unittest.TestCase):
    """Il lavoro di chi ripara e quello di chi controlla stanno nella stessa tabella."""

    def test_la_tabella_dei_lavori_aperti_ha_i_quattro_stati(self):
        stato = (TEMPLATES / "ecosystem-check" / "STATO.md").read_text(encoding="utf-8")
        self.assertIn("Lavori aperti", stato)
        for st in ("DA VERIFICARE", "CHIUSO", "BOCCIATO", "AL PROPRIETARIO"):
            self.assertIn(st, stato)
        self.assertIn("senza prova non puo' essere `CHIUSO`", stato)

    def test_il_controllo_comanda_il_lavoro_della_manutenzione(self):
        """Sal, 18/09/2026: chi vede tutta la casa dice cosa togliere e cosa sistemare."""
        stato = (TEMPLATES / "ecosystem-check" / "STATO.md").read_text(encoding="utf-8")
        self.assertIn("DA FARE", stato)
        self.assertIn("Chi ha eseguito non giudica il proprio lavoro", stato)
        ispettore = leggi("ISPETTORE_SKILL.md")
        self.assertIn("le righe\n`DA FARE`", ispettore)
        self.assertIn("le tre cose che pesano di piu'", ispettore)

    def test_il_manutentore_scrive_da_verificare_e_riparte_dalle_bocciate(self):
        testo = leggi("MANUTENTORE_SKILL.md")
        self.assertIn("Lavori aperti", testo)
        self.assertIn("esegui nell'ordine le righe `DA FARE`", testo)
        self.assertIn("Non scriverti `CHIUSO` da solo", testo)

    def test_l_ispettore_chiude_o_boccia_il_lunedi(self):
        testo = leggi("ISPETTORE_SKILL.md")
        self.assertIn("Lavori aperti", testo)
        self.assertIn("`DA VERIFICARE`", testo)
        self.assertIn("non e' una prova", testo)
        self.assertIn("AL PROPRIETARIO", testo)

    def test_la_tabella_resta_corta(self):
        """Un registro che cresce all'infinito non lo legge nessuno."""
        self.assertIn("sette giorni", (TEMPLATES / "ecosystem-check" / "STATO.md").read_text(encoding="utf-8"))
        self.assertIn("piu' vecchie di sette giorni si", leggi("MANUTENTORE_SKILL.md"))


class SaComeERiparareTest(unittest.TestCase):
    """Sal, 18/09/2026: «deve ragionare e capire», non seguire un elenco."""

    def test_la_casa_dichiara_come_e_messa_in_piedi(self):
        pagina = leggi("COME_E_MESSA_IN_PIEDI.md")
        for parte in ("Le istruzioni", "La memoria", "I guardiani",
                      "Le attivita' che partono da sole"):
            self.assertIn(parte, pagina)
        self.assertIn("Cosa vuol dire «sano»", pagina)
        self.assertIn("Riparato senza riprova non esiste", pagina)

    def test_il_manutentore_ragiona_da_quella_pagina(self):
        testo = leggi("MANUTENTORE_SKILL.md")
        self.assertIn("COME_E_MESSA_IN_PIEDI.md", testo)
        self.assertIn("Non applicare un\nelenco di comandi", testo)


class LaMappaNominaIManualiTest(unittest.TestCase):
    """Sal, 18/09/2026: «dovremmo installare un manuale che devono leggere dentro la casa».

    Prima la mappa madre del cliente non nominava nessuno dei quattro documenti:
    l'assistente poteva vivere nella casa senza aprirli mai.
    """

    def test_la_mappa_madre_porta_ai_quattro_manuali(self):
        mappa = leggi("AGENTS.md")
        for documento in ("Manutentore", "Ispettore",
                          "COME_E_MESSA_IN_PIEDI.md", "COSA_E_ACCESO.md"):
            self.assertIn(documento, mappa)
        self.assertIn("Lavori aperti", mappa)
        self.assertIn("Chi lavora in questa casa", mappa)
        self.assertIn("si corregge il suo manuale", " ".join(mappa.split()))
        self.assertLessEqual(len(mappa.splitlines()), 350, "la mappa madre non sfora il tetto")


class FoglioDeiPassaggiTest(unittest.TestCase):
    """Sal, 18/09/2026: «un foglio dove mettiamo tutti i passaggi che facciamo,
    cosi' l'Ispettore puo' verificare»."""

    def test_il_foglio_chiede_come_si_controlla_ogni_passaggio(self):
        foglio = leggi("PASSAGGI.md")
        for colonna in ("Quando", "Chi", "Cosa ha fatto", "Come si controlla", "Verificato"):
            self.assertIn(colonna, foglio)
        self.assertIn("Chi ha fatto il passaggio non si verifica da solo", foglio)
        self.assertIn("mentre", foglio)

    def test_l_ispettore_verifica_il_foglio_e_il_manutentore_lo_riempie(self):
        ispettore = " ".join(leggi("ISPETTORE_SKILL.md").split())
        manutentore = " ".join(leggi("MANUTENTORE_SKILL.md").split())
        self.assertIn("PASSAGGI.md", ispettore)
        self.assertIn("apri una riga `DA FARE`", ispettore)
        self.assertIn("PASSAGGI.md", manutentore)
        self.assertIn("La colonna `Verificato` non la tocchi", manutentore)


if __name__ == "__main__":
    unittest.main()
