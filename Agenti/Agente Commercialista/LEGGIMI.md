# Agente Commercialista

Ruolo operativo per chi vuole tenere sotto controllo posizione fiscale,
documenti, comunicazioni e scadenze con il proprio agente AI.

L'agente cerca le prove gia' disponibili, aggiorna una sola fonte, prepara il
lavoro fino all'ultimo clic e chiude soltanto con ricevuta o prova equivalente.
Il titolare gestisce accessi e azioni irreversibili; il professionista abilitato
decide e firma cio' che la legge gli riserva.

## Scheda del ruolo

| Campo | Valore |
|---|---|
| Attivazione | A chiamata con `Lancia l'Agente Commercialista` o su richieste fiscali; puo' entrare in una routine gia' esistente dopo il censimento |
| Fonte | Un solo `SCADENZARIO_FISCALE.md` nella stanza che possiede amministrazione e fiscalita' |
| Risultato | Posizione provata, prossima azione, documenti recuperati, adempimento pronto all'ultimo clic |
| Controllo | Eventi senza azione, scadenze vicine, chiusure senza prova, documenti mancanti o scaduti |
| Arresto | Login/OTP, firma, pagamento, dichiarazione, invio irreversibile, scelta fiscale o intervento professionale |

## Cosa contiene

- `INSTALLA_CON_AI.md`: installazione guidata nella casa esistente.
- `SCADENZARIO_FISCALE_TEMPLATE.md`: calco della fonte operativa unica.
- `PROCEDURA.md`: comportamento comune, senza aliquote o date hardcoded.
- `SKILL.md`: skill per Codex o agente compatibile.
- `AGENTE_CLAUDE.md` e `AGENTE_CODEX.toml`: adattatori nativi sottili.

Il pacchetto non contiene dati fiscali, credenziali o calendario di una persona.
Le regole si verificano nelle fonti ufficiali correnti; la posizione si verifica
nei documenti intestati e nei portali autenticati del titolare.
