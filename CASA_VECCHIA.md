# Hai la casa vecchia? Come aggiornarla

Versione corrente: `0.7.16`

Questa pagina serve quando nella cartella del proprietario c'e' gia' una casa
nata con una versione precedente. La riconosci cosi': `VERSION` inizia con
`0.6`, oppure ci sono `AGENTS.md`, `memory/`, `ecosistema/` e i guardiani in
`.agent/hooks/` ma mancano `README.md` e `logs/install-state.json`.

Quella casa contiene programmi e impostazioni che il pacchetto corrente non
porta piu'. Non si butta e non se ne crea una seconda accanto: si aggiorna, e
si toglie il vecchio soltanto dopo aver provato il nuovo. Tutto quello che serve
sta nella cartella `4 Gestione dell'ecosistema`:
<https://drive.google.com/drive/folders/1wdSNouSCbuF7G8Ab_m8R_Kw0uGnphc2Q>.

## Fai queste cose, in quest'ordine

1. **Inventario, senza toccare niente.** Elenca in `logs/install-log.md` cosa
   c'e': documenti compilati dal proprietario (memoria, fonti, processi, limiti,
   note) e pezzi LeaderAI (guardiani in `.agent/hooks/`, impostazioni
   dell'assistente, registro git, attivita' giornaliera di manutenzione).
2. **Copia completa, prima di tutto.** Fai un archivio zip datato dell'intera
   cartella cosi' com'e', compresi i file nascosti e la cartella `.git`, e
   mettilo fuori dalla casa (in Download o in una cartella scelta dal
   proprietario). Serve a tornare indietro: si tiene finche' il proprietario non
   ha usato la casa aggiornata per una settimana. Non e' la copia di sicurezza
   quotidiana: quella arriva al passo 4.
3. **Metti in pausa la vecchia macchina.** Ferma attivita' programmate,
   manutenzione automatica e guardiani finche' l'aggiornamento non e' provato.
   Non installare o riaccendere nulla in questa fase.
4. **Applica il Passo 1 corrente.** Segui `01 - Cervello - installazione e
   aggiornamento`, ramo casa esistente: aggiungi soltanto i documenti mancanti
   del pacchetto corrente, non sostituire quelli compilati e non cambiare
   impostazioni del computer. Scrivi la nuova versione soltanto alla fine.
5. **Prova la base documentale.** Apri l'assistente in una chat nuova dentro la
   casa e chiedi tre cose: chi e' il proprietario, cosa c'e' in memoria, cosa e'
   stato fatto oggi. Deve rispondere dai documenti aggiornati.
6. **Se la prova fallisce, torna indietro.** Ripristina la copia del passo 2,
   annota il punto che non ha funzionato e riprova senza eliminare nulla.
7. **Solo dopo separa il vecchio tecnico.** Se la prova riesce, disattiva o
   archivia i vecchi hook e le vecchie impostazioni LeaderAI che non fanno parte
   del Passo 1. Se ne trovi nelle impostazioni generali dell'assistente,
   toglili da li': non devono bloccare chat aperte altrove. Non sostituirli con
   componenti nuovi durante la migrazione.
8. **Togli il registro git soltanto dopo la prova.** Chiedi al proprietario un
   solo gesto: cancellare la cartella `.git` e il file `.gitignore`. La casa non
   e' un repository: niente clone, pull o push.
9. **Tieni una sola casa.** Se lavora da piu' computer, la casa vive in una
   cartella condivisa (OneDrive, Google Drive o iCloud) marcata «sempre
   disponibile offline» su ogni computer, una macchina alla volta.
10. **Rimanda la tecnica al Passo 4.** Backup quotidiano, guardiani,
   manutenzione, skill e impostazioni si valutano piu' avanti, uno per volta.
   Per ciascuno il proprietario deve vedere cosa fa, dove vive, come si prova e
   come si spegne. Non sono prerequisiti per aggiornare il Cervello.

La prova del passo 5 sostituisce il vecchio collaudo tecnico. Non aprire il
Passo 4 durante questa migrazione.

## Alla fine

Di' al proprietario in una frase cosa hai fatto, e aggiungi questo consiglio con
queste parole: «Ti consiglio di tenere questa cartella dentro una cartella
online (OneDrive, Google Drive o iCloud) oppure di farne una copia ogni tanto.
Decidi tu.» E' un consiglio, non un obbligo: se sceglie di non farlo, la casa
funziona lo stesso.
