# Hai la casa vecchia? Come aggiornarla

Versione corrente: `0.7.13`

Questa pagina serve quando nella cartella del proprietario c'e' gia' una casa
nata con una versione precedente. La riconosci cosi': `VERSION` inizia con
`0.6`, oppure ci sono `AGENTS.md`, `memory/`, `ecosistema/` e i guardiani in
`.agent/hooks/` ma mancano `README.md` e `logs/install-state.json`.

Quella casa contiene programmi e impostazioni che il pacchetto corrente non
porta piu'. Non si butta e non se ne crea una seconda accanto: si aggiorna.
Tutto quello che serve sta nella cartella `4 Gestione dell'ecosistema`:
<https://drive.google.com/drive/folders/1wdSNouSCbuF7G8Ab_m8R_Kw0uGnphc2Q>.

## Fai queste cose, in quest'ordine

1. **Prima la copia di sicurezza.** Prendi `BACKUP_CASA.py` da
   `4 Gestione dell'ecosistema`, mettilo in `.agent/hooks/backup_casa.py` e fai
   la prima copia in una cartella fuori dalla casa, scelta dal proprietario:
   `python3 .agent/hooks/backup_casa.py --imposta "<cartella>"` (su Windows
   `py` al posto di `python3`). Segreti e archivi protetti restano fuori.
2. **Il registro git si toglie.** La casa non e' un registro git: e' una
   decisione fissa di LeaderAI. Fatta la copia, chiedi al proprietario un solo
   gesto: cancellare la cartella `.git` (e `.gitignore`). Niente clone, pull o
   push. Se lavora da piu' computer, la casa vive in una cartella condivisa
   (OneDrive, Google Drive o iCloud) marcata «sempre disponibile offline» su
   ogni computer, e si lavora da una macchina alla volta.
3. **I guardiani devono rispondere.** Apri `GUARDIANI.md` in
   `4 Gestione dell'ecosistema` e fai la prova che c'e' scritta: un file a caso
   fuori posto nella casa, poi chiedi di chiudere il lavoro. Deve fermarsi. Se
   non si ferma su Windows, nelle impostazioni della casa sostituisci `python3`
   con `py` e riprova. Se i file della casa hanno in testa i tre byte invisibili
   (BOM), toglili senza cambiare il contenuto.
4. **I guardiani stanno solo nella casa.** Se ne trovi copiati nelle
   impostazioni generali dell'assistente sul computer, quelle che valgono per
   ogni cartella, toglili da li': bloccano ogni chat aperta altrove. Li' resta
   soltanto l'indicazione della memoria.
5. **Porta nella casa i documenti nuovi** di `4 Gestione dell'ecosistema` che
   mancano: `GUARDIANI.md`, `COSA_E_ACCESO.md`, `COME_E_MESSA_IN_PIEDI.md` e
   `PASSAGGI.md` vanno in `ecosistema/`. Aggiorna «cosa e' acceso» con quello
   che davvero parte da solo.
6. **Poi la guida normale.** Segui `01 - Cervello - installazione e
   aggiornamento`, ramo casa esistente: aggiungi i file mancanti del pacchetto
   corrente, non sostituire i documenti compilati, scrivi `VERSION` soltanto
   alla fine.

## Alla fine

Di' al proprietario in una frase cosa hai fatto, e aggiungi questo consiglio con
queste parole: «Ti consiglio di tenere questa cartella dentro una cartella
online (OneDrive, Google Drive o iCloud) oppure di farne una copia ogni tanto.
Decidi tu.» E' un consiglio, non un obbligo: se sceglie di non farlo, la casa
funziona lo stesso.
