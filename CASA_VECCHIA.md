# Hai la casa vecchia? Come aggiornarla

Versione corrente: `0.7.15`

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
3. **Ferma l'attivita' giornaliera.** Se nell'app dell'assistente c'e'
   l'attivita' programmata di manutenzione della casa, mettila in pausa finche'
   l'aggiornamento non e' provato.
4. **Copia di sicurezza quotidiana.** Prendi `BACKUP_CASA.py` da
   `4 Gestione dell'ecosistema`, mettilo in `.agent/hooks/backup_casa.py` e fai
   la prima copia in una cartella fuori dalla casa, scelta dal proprietario:
   `python3 .agent/hooks/backup_casa.py --imposta "<cartella>"` (su Windows
   `py` al posto di `python3`). Segreti e archivi protetti restano fuori.
5. **I guardiani devono rispondere.** Apri `GUARDIANI.md` in
   `4 Gestione dell'ecosistema` e fai la prova che c'e' scritta: un file a caso
   fuori posto nella casa, poi chiedi di chiudere il lavoro. Deve fermarsi. Se
   non si ferma su Windows, nelle impostazioni della casa sostituisci `python3`
   con `py` e riprova. Se i file della casa hanno in testa i tre byte invisibili
   (BOM), toglili senza cambiare il contenuto.
6. **I guardiani stanno solo nella casa.** Se ne trovi copiati nelle
   impostazioni generali dell'assistente sul computer, quelle che valgono per
   ogni cartella, toglili da li': bloccano ogni chat aperta altrove. Li' resta
   soltanto l'indicazione della memoria.
7. **Porta nella casa i documenti nuovi** di `4 Gestione dell'ecosistema` che
   mancano: `GUARDIANI.md`, `COSA_E_ACCESO.md`, `COME_E_MESSA_IN_PIEDI.md` e
   `PASSAGGI.md` vanno in `ecosistema/`.
8. **Poi la guida normale.** Segui `01 - Cervello - installazione e
   aggiornamento`, ramo casa esistente: aggiungi i file mancanti del pacchetto
   corrente, non sostituire i documenti compilati, scrivi `VERSION` soltanto
   alla fine.
9. **Prova, e solo dopo togli il registro git.** Apri l'assistente in una chat
   nuova dentro la casa e chiedi tre cose: chi e' il proprietario, cosa c'e' in
   memoria, cosa e' stato fatto oggi. Deve rispondere dai documenti aggiornati.
   Solo se risponde, chiedi al proprietario un solo gesto: cancellare la
   cartella `.git` (e `.gitignore`). La casa non e' un registro git: decisione
   fissa di LeaderAI. Niente clone, pull o push. Se lavora da piu' computer, la
   casa vive in una cartella condivisa (OneDrive, Google Drive o iCloud) marcata
   «sempre disponibile offline» su ogni computer, una macchina alla volta. Se
   qualcosa non torna, si rimette la copia del passo 2 e si riprova.
10. **Riaccendi l'attivita' giornaliera** fermata al passo 3 e aggiorna «cosa e'
    acceso» con quello che davvero parte da solo.

## Alla fine

Di' al proprietario in una frase cosa hai fatto, e aggiungi questo consiglio con
queste parole: «Ti consiglio di tenere questa cartella dentro una cartella
online (OneDrive, Google Drive o iCloud) oppure di farne una copia ogni tanto.
Decidi tu.» E' un consiglio, non un obbligo: se sceglie di non farlo, la casa
funziona lo stesso.
