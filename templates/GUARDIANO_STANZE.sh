#!/usr/bin/env bash

# Guardiano deterministico LeaderAI: impedisce a Codex e Claude di chiudere
# un turno lasciando file, cartelle o copie fuori dal contratto della casa.

set -u
export LC_ALL=C

HOOK_INPUT="$(cat 2>/dev/null || printf '{}')"
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" 2>/dev/null && pwd)"
ROOT="$(CDPATH= cd -- "$SCRIPT_DIR/../.." 2>/dev/null && pwd)"

if [ -z "$ROOT" ] || [ ! -d "$ROOT" ]; then
    printf '%s\n' "BLOCCO STRUTTURA: cartella madre non individuata." >&2
    exit 2
fi

STOP_HOOK_ACTIVE=false
if printf '%s' "$HOOK_INPUT" | grep -Eq '(^|[,{])[[:space:]]*"stop_hook_active"[[:space:]]*:[[:space:]]*true([[:space:]]*[,}])'; then
    STOP_HOOK_ACTIVE=true
fi

ISSUES_FILE="$(mktemp "${TMPDIR:-/tmp}/leaderai-guardiano.XXXXXX" 2>/dev/null)" || {
    if [ "$STOP_HOOK_ACTIVE" = true ]; then
        printf '%s\n' '{"systemMessage":"Il controllo finale della struttura non e stato eseguito: riprova prima di modificare altri file."}'
        exit 0
    fi
    printf '%s\n' "BLOCCO STRUTTURA: controllo finale non avviato." >&2
    exit 2
}
trap 'rm -f -- "$ISSUES_FILE"' EXIT HUP INT TERM

add_issue() {
    printf '%s\n' "$1" >> "$ISSUES_FILE"
}

relative_path() {
    case "$1" in
        "$ROOT") printf '.\n' ;;
        "$ROOT"/*) printf '%s\n' "${1#"$ROOT"/}" ;;
        *) printf '%s\n' "$1" ;;
    esac
}

has_exact_reference() {
    local file="$1"
    local target="$2"
    local section="${3:-}"
    [ -f "$file" ] || return 1
    awk -v target="$target" -v section="$section" '
        function clean(value) {
            sub(/\/$/, "", value)
            return value
        }
        BEGIN { active = (section == "") }
        {
            line = $0
            sub(/\r$/, "", line)
            if (section != "" && line == "## " section) {
                active = 1
                next
            }
            if (section != "" && active && line ~ /^## /) {
                exit(found ? 0 : 1)
            }
            if (!active) {
                next
            }
            rest = line
            while ((start = index(rest, "`")) > 0) {
                rest = substr(rest, start + 1)
                finish = index(rest, "`")
                if (finish == 0) {
                    break
                }
                token = clean(substr(rest, 1, finish - 1))
                if (token == target) {
                    found = 1
                }
                rest = substr(rest, finish + 1)
            }
            rest = line
            while ((start = index(rest, "](")) > 0) {
                rest = substr(rest, start + 2)
                finish = index(rest, ")")
                if (finish == 0) {
                    break
                }
                token = clean(substr(rest, 1, finish - 1))
                if (token == target) {
                    found = 1
                }
                rest = substr(rest, finish + 1)
            }
        }
        END { exit(found ? 0 : 1) }
    ' "$file"
}

is_registered_at_root() {
    local rel="$1"
    {
        root_owned_row "$ROOT/AGENTS.md" "$rel" "ecosistema/ASSET.md" &&
            detail_registry_row "$ROOT/ecosistema/ASSET.md" "$rel" "## Registro"
    } || {
        root_owned_row "$ROOT/AGENTS.md" "$rel" "ecosistema/FONTI.md" &&
            detail_registry_row "$ROOT/ecosistema/FONTI.md" "$rel" "## Fonti trovate"
    }
}

room_registered_at_root() {
    local file="$1"
    local target="$2"
    [ -f "$file" ] || return 1
    awk -F'|' -v target="$target" '
        function trim(value) {
            gsub(/^[[:space:]]+|[[:space:]]+$/, "", value)
            return value
        }
        function reference(cell, rest, start, finish) {
            cell = trim(cell)
            start = index(cell, "](")
            if (start > 0) {
                rest = substr(cell, start + 2)
                finish = index(rest, ")")
                if (finish > 0) return substr(rest, 1, finish - 1)
            }
            if (substr(cell, 1, 1) == "`" && substr(cell, length(cell), 1) == "`") {
                return substr(cell, 2, length(cell) - 2)
            }
            return cell
        }
        function meaningful(cell, normalized) {
            cell = trim(cell)
            normalized = tolower(cell)
            return cell != "" && cell != "-" && cell !~ /\{\{/ &&
                normalized !~ /^da (censire|definire|compilare|assegnare)/
        }
        {
            line = $0
            sub(/\r$/, "", line)
            if (line == "### Registro delle stanze") { active = 1; next }
            if (active && line ~ /^### /) exit
            if (!active || line !~ /^[[:space:]]*\|/) next
            count = split(line, cells, "|")
            if (count < 11) next
            room_path = reference(cells[2])
            sub(/\/$/, "", room_path)
            map_path = reference(cells[9])
            if (room_path == target && meaningful(cells[3]) && map_path == target "/AGENTS.md" && meaningful(cells[10]) && meaningful(cells[11])) found = 1
        }
        END { exit(found ? 0 : 1) }
    ' "$file"
}

root_owned_row() {
    local file="$1"
    local target="$2"
    local registry="$3"
    [ -f "$file" ] || return 1
    awk -F'|' -v target="$target" -v registry="$registry" '
        function trim(value) {
            gsub(/^[[:space:]]+|[[:space:]]+$/, "", value)
            return value
        }
        function reference(cell) {
            cell = trim(cell)
            if (substr(cell, 1, 1) == "`" && substr(cell, length(cell), 1) == "`") {
                return substr(cell, 2, length(cell) - 2)
            }
            return cell
        }
        function meaningful(cell, normalized) {
            cell = trim(cell)
            normalized = tolower(cell)
            return cell != "" && cell != "-" && cell !~ /\{\{/ &&
                normalized !~ /^da (censire|definire|compilare|assegnare)/
        }
        {
            line = $0
            sub(/\r$/, "", line)
            if (line == "### Elementi posseduti direttamente dalla cartella madre") {
                active = 1
                next
            }
            if (active && line ~ /^### /) exit
            if (!active || line !~ /^[[:space:]]*\|/) next
            count = split(line, cells, "|")
            if (count < 5) next
            path = reference(cells[2])
            sub(/\/$/, "", path)
            class = toupper(reference(cells[3]))
            detail = reference(cells[5])
            if (path == target && class ~ /^(FONTE|OUTPUT|CAPACITA|INFRASTRUTTURA|ARCHIVIO)$/ && meaningful(cells[4]) && detail == registry) found = 1
        }
        END { exit(found ? 0 : 1) }
    ' "$file"
}

detail_registry_row() {
    local file="$1"
    local target="$2"
    local section="$3"
    [ -f "$file" ] || return 1
    awk -F'|' -v target="$target" -v section="$section" '
        function trim(value) {
            gsub(/^[[:space:]]+|[[:space:]]+$/, "", value)
            return value
        }
        function has_reference(cell, rest, start, finish, token) {
            rest = cell
            while ((start = index(rest, "`")) > 0) {
                rest = substr(rest, start + 1)
                finish = index(rest, "`")
                if (finish == 0) break
                token = substr(rest, 1, finish - 1)
                sub(/\/$/, "", token)
                if (token == target) return 1
                rest = substr(rest, finish + 1)
            }
            rest = cell
            while ((start = index(rest, "](")) > 0) {
                rest = substr(rest, start + 2)
                finish = index(rest, ")")
                if (finish == 0) break
                token = substr(rest, 1, finish - 1)
                sub(/\/$/, "", token)
                if (token == target) return 1
                rest = substr(rest, finish + 1)
            }
            return 0
        }
        function meaningful(cell, normalized) {
            cell = trim(cell)
            normalized = tolower(cell)
            return cell != "" && cell != "-" && cell !~ /^-+$/ && cell !~ /\{\{/ &&
                normalized !~ /^da (censire|definire|compilare|assegnare)/
        }
        {
            line = $0
            sub(/\r$/, "", line)
            if (line == section) { active = 1; next }
            if (active && line ~ /^## /) exit
            if (!active || line !~ /^[[:space:]]*\|/) next
            count = split(line, cells, "|")
            referenced = 0
            filled = 0
            for (i = 2; i < count; i++) {
                if (has_reference(cells[i])) referenced = 1
                if (meaningful(cells[i])) filled++
            }
            if (referenced && filled >= 4) found = 1
        }
        END { exit(found ? 0 : 1) }
    ' "$file"
}

valid_bridge() {
    local bridge="$1"
    local lines content
    [ -f "$bridge" ] || return 1
    lines="$(wc -l < "$bridge" | tr -d '[:space:]')"
    content="$(tr -d '\r\n' < "$bridge")"
    [ "$lines" = "1" ] && [ "$content" = "@AGENTS.md" ]
}

section_has_meaningful_content() {
    local file="$1"
    local heading="$2"
    [ -f "$file" ] || return 1
    awk -v heading="$heading" '
        function trim(value) {
            gsub(/^[[:space:]]+|[[:space:]]+$/, "", value)
            return value
        }
        {
            line = $0
            sub(/\r$/, "", line)
            if (line == "## " heading) { active = 1; next }
            if (active && line ~ /^## /) exit
            if (!active) next
            raw = trim(line)
            if (raw == "") next
            value = raw
            sub(/^[-*>][[:space:]]*/, "", value)
            normalized = tolower(trim(value))
            valid = normalized != "" && normalized != "-" && normalized !~ /\{\{/ && normalized !~ /^(todo|tbd)(:|$)/ && normalized !~ /^da (censire|definire|compilare|collegare|assegnare)([ .:]|$)/ && normalized !~ /^descrivere la funzione aziendale/
            if (heading == "Dentro") {
                valid = normalized == "nessuna sottocartella" || value ~ /^`[^`]+`/
            } else if (heading == "Fonte business editabile") {
                valid = value ~ /^`[^`]+`/ || normalized ~ /^non applicabile:[[:space:]]*[^[:space:]]/
            }
            if (valid) found = 1
            exit(found ? 0 : 1)
        }
        END { exit(found ? 0 : 1) }
    ' "$file"
}

section_first_value() {
    local file="$1"
    local heading="$2"
    awk -v heading="$heading" '
        function trim(value) {
            gsub(/^[[:space:]]+|[[:space:]]+$/, "", value)
            return value
        }
        {
            line = $0
            sub(/\r$/, "", line)
            if (line == "## " heading) { active = 1; next }
            if (active && line ~ /^## /) exit
            if (!active) next
            value = trim(line)
            if (value == "") next
            sub(/^[-*>][[:space:]]*/, "", value)
            print trim(value)
            exit
        }
    ' "$file"
}

section_code_references() {
    local file="$1"
    local heading="$2"
    awk -v heading="$heading" '
        {
            line = $0
            sub(/\r$/, "", line)
            if (line == "## " heading) { active = 1; next }
            if (active && line ~ /^## /) exit
            if (!active) next
            rest = line
            while ((start = index(rest, "`")) > 0) {
                rest = substr(rest, start + 1)
                finish = index(rest, "`")
                if (finish == 0) break
                print substr(rest, 1, finish - 1)
                rest = substr(rest, finish + 1)
            }
        }
    ' "$file"
}

portable_relative_path() {
    case "$1" in
        ""|/*|.*|*\\*|..|../*|*/..|*/../*) return 1 ;;
        *) return 0 ;;
    esac
}

path_has_symlink_component() {
    local base="$1"
    local relative="$2"
    local current="$base"
    local part
    local -a parts
    IFS='/' read -r -a parts <<< "$relative"
    for part in "${parts[@]}"; do
        current="$current/$part"
        [ -L "$current" ] && return 0
    done
    return 1
}

validate_room_map() {
    local room="$1"
    local rel="$2"
    local map="$room/AGENTS.md"
    local heading source child child_name source_heading declared_child business_value business_path
    [ -f "$map" ] || return 0

    if grep -Fq -- '{{' "$map"; then
        add_issue "$rel/AGENTS.md - mappa con campi del calco non compilati"
    fi
    for heading in \
        "Stato corrente e prossimo passo" \
        "Scopo" \
        "Responsabilita business" \
        "Organigramma" \
        "Dentro" \
        "Fonti" \
        "Output" \
        "Fonte operativa" \
        "Fonte business editabile" \
        "Capacita" \
        "A monte" \
        "A valle" \
        "Dove scrivere" \
        "Regole"
    do
        if ! sed 's/\r$//' "$map" | grep -Fqx -- "## $heading"; then
            add_issue "$rel/AGENTS.md - sezione obbligatoria mancante: $heading"
        elif ! section_has_meaningful_content "$map" "$heading"; then
            add_issue "$rel/AGENTS.md - sezione senza contenuto utile: $heading"
        fi
    done

    source="$({
        awk '
            {
                line = $0
                sub(/\r$/, "", line)
                if (line == "## Fonte operativa") { active = 1; next }
                if (active && line ~ /^## /) { exit }
                if (active) {
                    start = index(line, "`")
                    if (start > 0) {
                        rest = substr(line, start + 1)
                        finish = index(rest, "`")
                        if (finish > 0) {
                            print substr(rest, 1, finish - 1)
                            exit
                        }
                    }
                }
            }
        ' "$map"
    } 2>/dev/null)"
    case "$source" in
        ""|/*|..|../*|*/..|*/../*)
            add_issue "$rel/AGENTS.md - fonte operativa assente o non portabile"
            ;;
        *)
            if ! portable_relative_path "$source" || path_has_symlink_component "$room" "$source"; then
                add_issue "$rel/$source - fonte operativa non locale o collegata"
            elif [ ! -f "$room/$source" ]; then
                add_issue "$rel/$source - fonte operativa dichiarata ma assente"
            else
                if grep -Fq -- '{{' "$room/$source"; then
                    add_issue "$rel/$source - fonte operativa con campi non compilati"
                fi
                for source_heading in "Stato corrente" "Prossimo passo" "Decisioni" "Scadenze"; do
                    if ! sed 's/\r$//' "$room/$source" | grep -Fqx -- "## $source_heading"; then
                        add_issue "$rel/$source - sezione obbligatoria mancante: $source_heading"
                    elif ! section_has_meaningful_content "$room/$source" "$source_heading"; then
                        add_issue "$rel/$source - sezione senza contenuto utile: $source_heading"
                    fi
                done
            fi
            ;;
    esac

    while IFS= read -r declared_child; do
        declared_child="${declared_child%/}"
        if ! portable_relative_path "$declared_child" || [[ "$declared_child" == */* ]]; then
            add_issue "$rel/AGENTS.md - percorso Dentro non valido: $declared_child"
        elif [ ! -d "$room/$declared_child" ] || [ -L "$room/$declared_child" ]; then
            add_issue "$rel/$declared_child - sottocartella dichiarata ma assente o collegata"
        fi
    done < <(section_code_references "$map" "Dentro")

    business_value="$(section_first_value "$map" "Fonte business editabile")"
    case "$business_value" in
        [Nn][Oo][Nn]' '[Aa][Pp][Pp][Ll][Ii][Cc][Aa][Bb][Ii][Ll][Ee]:*) ;;
        \`*\`*)
            business_path="${business_value#\`}"
            business_path="${business_path%%\`*}"
            if ! portable_relative_path "$business_path" || path_has_symlink_component "$room" "$business_path"; then
                add_issue "$rel/$business_path - fonte business non locale o collegata"
            elif [ ! -f "$room/$business_path" ]; then
                add_issue "$rel/$business_path - fonte business dichiarata ma assente"
            elif [ ! -s "$room/$business_path" ] || grep -Fq -- '{{' "$room/$business_path"; then
                add_issue "$rel/$business_path - fonte business vuota o non compilata"
            fi
            ;;
    esac

    while IFS= read -r -d '' child; do
        child_name="$(basename -- "$child")"
        case "$child_name" in
            .*|node_modules|venv|__pycache__|vendor) continue ;;
        esac
        if ! has_exact_reference "$map" "$child_name" "Dentro"; then
            add_issue "$rel/$child_name - sottocartella non dichiarata nella sezione Dentro"
        fi
    done < <(find "$room" -mindepth 1 -maxdepth 1 -type d ! -name '.*' -print0 2>/dev/null)
}

# L'armadio comune contiene soltanto i sei file canonici.
if [ ! -d "$ROOT/ecosistema" ]; then
    add_issue "ecosistema/ - armadio comune mancante"
else
    while IFS= read -r -d '' item; do
        name="$(basename -- "$item")"
        case "$name" in
            FONTI.md|ASSET.md|PROCESSI.md|LIMITI.md|STANZA_AGENTS.md|STANZA_FONTE.md) ;;
            *) add_issue "$(relative_path "$item") - elemento non ammesso nell'armadio comune" ;;
        esac
    done < <(find "$ROOT/ecosistema" -mindepth 1 -maxdepth 1 -print0 2>/dev/null)
fi

# Ogni elemento visibile nella cartella madre ha un proprietario dichiarato.
while IFS= read -r -d '' item; do
    rel="$(relative_path "$item")"
    case "$rel" in
        AGENTS.md|CLAUDE.md|AGENT_CHAT.md|ecosistema|memory|logs) continue ;;
    esac

    if [ -d "$item" ] && { [ -e "$item/AGENTS.md" ] || [ -e "$item/CLAUDE.md" ]; }; then
        [ -f "$item/AGENTS.md" ] || add_issue "$rel/AGENTS.md - mappa della stanza mancante"
        [ -f "$item/CLAUDE.md" ] || add_issue "$rel/CLAUDE.md - ponte della stanza mancante"
        if [ -f "$item/CLAUDE.md" ] && ! valid_bridge "$item/CLAUDE.md"; then
            add_issue "$rel/CLAUDE.md - il ponte deve contenere soltanto @AGENTS.md"
        fi
        if ! room_registered_at_root "$ROOT/AGENTS.md" "$rel"; then
            add_issue "$rel - stanza non registrata nella mappa madre"
        fi
        validate_room_map "$item" "$rel"
        continue
    fi

    if ! is_registered_at_root "$rel"; then
        add_issue "$rel - elemento sciolto senza proprietario e registro"
    fi
done < <(find "$ROOT" -mindepth 1 -maxdepth 1 ! -name '.*' -print0 2>/dev/null)

# Nessun percorso della casa puo' essere invisibile al proprietario
# (macOS `chflags hidden`, Windows attributo Hidden). Dotfile esclusi.
is_hidden_from_owner() {
    local path="$1"
    local flags
    if flags="$(stat -f '%Sf' -- "$path" 2>/dev/null)"; then
        case ",$flags," in *,hidden,*) return 0 ;; esac
        return 1
    fi
    if command -v attrib >/dev/null 2>&1; then
        case "$(attrib "$path" 2>/dev/null | cut -c1-12)" in *H*) return 0 ;; esac
    fi
    return 1
}

while IFS= read -r -d '' visible_item; do
    if is_hidden_from_owner "$visible_item"; then
        add_issue "$(relative_path "$visible_item") - nascosto al proprietario: togliere il flag (chflags nohidden / attrib -h)"
    fi
done < <(
    find "$ROOT" -mindepth 1 -maxdepth 2 \
        \( -type d \( -name '.*' -o -name .venv -o -name venv -o -name node_modules -o -name __pycache__ -o -name vendor \) -prune \) -o \
        ! -name '.*' -print0 2>/dev/null
)

# Le mappe corte non possono diventare archivi paralleli.
while IFS= read -r -d '' router; do
    lines="$(wc -l < "$router" | tr -d '[:space:]')"
    bytes="$(wc -c < "$router" | tr -d '[:space:]')"
    if [ "$lines" -gt 350 ] || [ "$bytes" -gt 24576 ]; then
        add_issue "$(relative_path "$router") - mappa oltre il limite di 350 righe o 24 KiB"
    fi
done < <(
    find "$ROOT" \
        \( -type d \( -name .git -o -name .agent -o -name .agents -o -name .codex -o -name .claude -o -name .venv -o -name venv -o -name node_modules -o -name __pycache__ -o -name .secrets -o -name vendor \) -prune \) -o \
        -type f \( -name AGENTS.md -o -name MEMORY.md -o -name AGENT_CHAT.md \) -print0 2>/dev/null
)

# Copie e nomi di versione non possono diventare nuove fonti vive.
while IFS= read -r -d '' candidate; do
    name="$(basename -- "$candidate" | tr '[:upper:]' '[:lower:]')"
    if printf '%s\n' "$name" | grep -Eq '(^|[_ .-])(v[0-9]+|finale?|copy|copia|\([0-9]+\))(\.[^.]+)?$'; then
        add_issue "$(relative_path "$candidate") - possibile copia o versione parallela"
    fi
done < <(
    find "$ROOT" \
        \( -type d \( -name .git -o -name .agent -o -name .agents -o -name .codex -o -name .claude -o -name .venv -o -name venv -o -name node_modules -o -name __pycache__ -o -name .secrets -o -name vendor \) -prune \) -o \
        -type f -print0 2>/dev/null
)

# Una cartella organizzativa vuota non regge una responsabilita reale.
while IFS= read -r -d '' empty_dir; do
    add_issue "$(relative_path "$empty_dir")/ - cartella vuota"
done < <(
    find "$ROOT" -mindepth 1 \
        \( -type d \( -name .git -o -name .agent -o -name .agents -o -name .codex -o -name .claude -o -name .venv -o -name venv -o -name node_modules -o -name __pycache__ -o -name .secrets -o -name vendor \) -prune \) -o \
        -type d -empty -print0 2>/dev/null
)

if [ ! -s "$ISSUES_FILE" ]; then
    exit 0
fi

if [ "$STOP_HOOK_ACTIVE" = true ]; then
    printf '%s\n' '{"systemMessage":"Il guardiano ha ancora trovato elementi fuori posto. I percorsi sono stati consegnati all agente nel passaggio precedente; serve chiuderli prima del prossimo lavoro."}'
    exit 0
fi

printf '%s\n' "BLOCCO STRUTTURA ECOSISTEMA" >&2
printf '%s\n' "Sistema questi percorsi prima di chiudere il lavoro:" >&2
while IFS= read -r issue; do
    printf ' - %s\n' "$issue" >&2
done < "$ISSUES_FILE"
printf '%s\n' "Modifica la fonte viva; non creare copie _v2 o _finale." >&2
exit 2
