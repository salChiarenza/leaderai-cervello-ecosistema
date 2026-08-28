# Standard di un reparto dell'Ecosistema

Questo e' il metro usato da Ecosystem Check. Vale per ogni reparto e per ogni
sottoreparto che possiede una responsabilita' autonoma.

## Quando nasce un reparto

Un reparto nasce soltanto quando mantiene una responsabilita' stabile, uno
stato corrente e decisioni proprie. Una cartella di file, una skill, uno script,
un output o una fonte non bastano.

## Cosa deve avere

1. `AGENTS.md` corto alla porta, con scopo, responsabilita', proprietario,
   contenuto, fonti, output, collegamenti e regole.
2. `CLAUDE.md` con la sola riga `@AGENTS.md`.
3. Una fonte operativa nominata, con in testa stato corrente, prossimo passo,
   decisioni e scadenze.
4. Un Amministratore del settore che riporta al Boss dell'Ecosistema.
5. Una riga nella mappa madre con un collegamento reale al reparto.
6. Ogni sottocartella diretta dichiarata in `Dentro` con la sua funzione.
7. Una sola fonte per ogni dato, stato o procedura.
8. Capacita' e collegamenti provati, non soltanto dichiarati.

## Dove deve vivere

- Un reparto vive al primo livello della cartella madre oppure dentro il reparto
  proprietario quando e' davvero un suo sottoreparto.
- `ecosistema/` contiene soltanto registri e calchi comuni. Nessun reparto,
  progetto, output o materiale operativo nasce al suo interno.
- Prima di creare si controlla se esiste gia' un proprietario adatto.

## Cosa blocca il controllo

- Cartella generica, vuota, doppia o senza proprietario.
- Reparto senza mappa, ponte, fonte operativa o collegamento alla radice.
- Sottocartella non dichiarata nella mappa locale.
- Stato o procedura copiati in piu' file.
- Materiale operativo dentro `ecosistema/`.
- Istruzioni che dichiarano capacita' o limiti senza una prova attuale.

## Igiene dei file

- `AGENTS.md`, `MEMORY.md` e `AGENT_CHAT.md`: massimo 350 righe o 24 KiB.
- Gli altri Markdown entrano in revisione oltre 800 righe o 80 KiB.
- Un file grande si accorcia quando mescola responsabilita', duplica fonti o
  contiene dettagli che appartengono a una procedura o a un reparto.
- Non si spezza un file solo per il numero di righe: prima si identifica la
  responsabilita' che non gli appartiene.

## Sequenza di creazione

1. Censire la casa e scegliere il proprietario.
2. Classificare il nuovo elemento.
3. Creare insieme mappa, ponte, fonte operativa e riga nella mappa madre.
4. Dichiarare tutte le sottocartelle dirette.
5. Provare almeno un percorso reale dalla richiesta all'output.
6. Eseguire Ecosystem Check e registrare l'esito.

Se uno dei passaggi manca, il reparto resta incompleto e non viene dichiarato
operativo.
