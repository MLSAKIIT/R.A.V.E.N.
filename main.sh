#!/usr/bin/env bash

# R.A.V.E.N - Rapid Automation & Vulnerability Enumeration for Networks
# Interactive launcher with themed menu

set -euo pipefail

# Basic settings
export PYTHONUNBUFFERED=1

# Color definitions
BRIGHT_RED='\033[1;31m'
CRIMSON='\033[38;5;196m'
ROYAL_BLUE='\033[38;5;21m'
ELECTRIC_BLUE='\033[38;5;33m'
DEEP_PURPLE='\033[38;5;55m'
VIOLET='\033[38;5;93m'
WHITE='\033[0;37m'
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
BOLD='\033[1m'
NC='\033[0m'

# detect python
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD=python
else
    PYTHON_CMD=python3
fi

# Resolve repository/script directory so paths work regardless of CWD or WSL mounts
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
SCRIPTS_DIR="$SCRIPT_DIR/scripts"

# Ctrl-C trap
trap 'echo; echo -e "${CRIMSON}Session terminated by user.${NC}"; stty sane 2>/dev/null || true; exit 0' INT

# Banner
show_banner() {
    printf "\033[2J\033[H"
    echo
    echo -e "${BRIGHT_RED}"
    cat << "EOF"
    ▄▄▄▄▄▄▄▄▄▄▄     ▄▄▄▄▄▄▄▄▄▄▄  ▄               ▄  ▄▄▄▄▄▄▄▄▄▄▄     ▄▄        ▄
   ▐░░░░░░░░░░░▌   ▐░░░░░░░░░░░▌▐░▌             ▐░▌▐░░░░░░░░░░░▌   ▐░░▌      ▐░▌
   ▐░█▀▀▀▀▀▀▀█░▌   ▐░█▀▀▀▀▀▀▀█░▌ ▐░▌           ▐░▌ ▐░█▀▀▀▀▀▀▀▀▀    ▐░▌░▌     ▐░▌
   ▐░▌       ▐░▌   ▐░▌       ▐░▌  ▐░▌         ▐░▌  ▐░▌             ▐░▌▐░▌    ▐░▌
   ▐░█▄▄▄▄▄▄▄█░▌   ▐░█▄▄▄▄▄▄▄█░▌   ▐░▌       ▐░▌   ▐░█▄▄▄▄▄▄▄▄▄    ▐░▌ ▐░▌   ▐░▌
   ▐░░░░░░░░░░░▌   ▐░░░░░░░░░░░▌    ▐░▌     ▐░▌    ▐░░░░░░░░░░░▌   ▐░▌  ▐░▌  ▐░▌
   ▐░█▀▀▀▀█░█▀▀    ▐░█▀▀▀▀▀▀▀█░▌     ▐░▌   ▐░▌     ▐░█▀▀▀▀▀▀▀▀▀    ▐░▌   ▐░▌ ▐░▌
   ▐░▌     ▐░▌     ▐░▌       ▐░▌      ▐░▌ ▐░▌      ▐░▌             ▐░▌    ▐░▌▐░▌
   ▐░▌      ▐░▌  ▄ ▐░▌       ▐░▌ ▄     ▐░▐░▌▄      ▐░█▄▄▄▄▄▄▄▄▄  ▄ ▐░▌     ▐░▐░▌ ▄
   ▐░▌       ▐░▌▐░▌▐░▌       ▐░▌▐░▌     ▐░▌▐░▌     ▐░░░░░░░░░░░▌▐░▌▐░▌      ▐░░▌▐░▌
    ▀         ▀  ▀  ▀         ▀  ▀       ▀  ▀       ▀▀▀▀▀▀▀▀▀▀▀  ▀  ▀        ▀▀  ▀
EOF
    echo -e "${NC}"
    echo
    echo -e "    ${CRIMSON}⟨ R.A.V.E.N. ⟩${NC} ${ROYAL_BLUE}Rapid Automation & Vulnerability Enumeration for Networks${NC}"
    echo
    echo
}

# Helper: safe run with tty mapping if available
_run_with_tty() {
    local cmd=("$@")
    local ttydev
    ttydev=$(tty 2>/dev/null) || ttydev=""
    if [ -n "$ttydev" ] && [ -c "$ttydev" ]; then
        local sttystate
        sttystate=$(stty -g 2>/dev/null) || sttystate=""
        stty sane 2>/dev/null || true
        "${cmd[@]}" <"$ttydev" >"$ttydev" 2>"$ttydev"
        local rc=$?
        if [ -n "$sttystate" ]; then stty "$sttystate" 2>/dev/null || true; else stty sane 2>/dev/null || true; fi
        return $rc
    else
        "${cmd[@]}"
        return $?
    fi
}

# Count scripts per category
declare -A script_counts
init_script_counts() {
    local cats=(crypto enumeration exploitation osint payloads scanning utils)
    for c in "${cats[@]}"; do
        if [ -d "$SCRIPTS_DIR/$c" ]; then
            script_counts["$c"]=$(find "$SCRIPTS_DIR/$c" -type f \( -name "*.py" -o -name "*.sh" \) 2>/dev/null | wc -l | tr -d ' ')
        else
            script_counts["$c"]=0
        fi
    done
}

get_script_count() { echo "${script_counts[$1]:-0}"; }

# Themed menu display
show_main_menu() {
    echo
    echo -e "                        ${BRIGHT_RED}⟨ SELECT ATTACK VECTOR ⟩${NC}"
    echo

    declare -A categories=(
        ["1"]="crypto:🔐 Cryptographic Tools:${BRIGHT_RED}"
        ["2"]="enumeration:📊 Service Enumeration Tools:${ROYAL_BLUE}"
        ["3"]="exploitation:💥 Exploit Tools and Payloads:${DEEP_PURPLE}"
        ["4"]="osint:🕵️ Open Source Intelligence:${CRIMSON}"
        ["5"]="payloads:🎯 Payload Generators:${ELECTRIC_BLUE}"
        ["6"]="scanning:🔍 Port Scanning and Service Detection:${VIOLET}"
        ["7"]="utils:🔧 General Utility Scripts:${BRIGHT_RED}"
    )

    for key in {1..7}; do
        IFS=':' read -r folder description color <<< "${categories[$key]}"
        script_count=$(get_script_count "$folder")
        if [[ $script_count -gt 0 ]]; then
            status="${ROYAL_BLUE}◆ ${script_count} LOADED${NC}"
        else
            status="${BRIGHT_RED}◇ AWAITING CONTRIBUTION${NC}"
        fi
        printf "   ${color}[%2s]${NC} ${WHITE}%-45s${NC} ${status}\n" "$key" "${description#* }"
    done
    echo
    echo -e "   ${CRIMSON}[99] ⟨ TERMINATE SESSION ⟩${NC}"
    echo
}

list_scripts() {
    local category=$1
    local label=$2
    if [ ! -d "$SCRIPTS_DIR/$category" ]; then
        echo
        echo -e "                        ${BRIGHT_RED}⟨ ${label^^} MODULE ⟩${NC}"
        echo
        echo -e "   ${ROYAL_BLUE}◇ NO EXPLOITS LOADED IN THIS MODULE${NC}"
        echo -e "   ${ROYAL_BLUE}◇ AWAITING CONTRIBUTION...${NC}"
        echo -e "   ${ROYAL_BLUE}◇ CHECK CONTRIBUTING.md FOR DEPLOYMENT GUIDE${NC}"
        echo
        read -r -p "Press Enter to continue..."
        return
    fi
    mapfile -t scripts < <(find "$SCRIPTS_DIR/$category" -maxdepth 2 -type f \( -name "*.py" -o -name "*.sh" \) 2>/dev/null | sort)
    if [ ${#scripts[@]} -eq 0 ]; then 
        echo -e "   ${ROYAL_BLUE}◇ NO EXPLOITS LOADED IN THIS MODULE${NC}"; echo
        read -r -p "Press Enter to continue..."
        return
    fi
    while true; do
        echo
        echo -e "                        ${BRIGHT_RED}⟨ ${label^^} TOOLKIT ⟩${NC}"
        echo
        local i=1
        for sp in "${scripts[@]}"; do
            name=$(basename "$sp")
            ext=${name##*.}
            printf "   ${CYAN}[%2d]${NC} ${WHITE}%s${NC} ${YELLOW}(%s)${NC}\n" "$i" "$name" "$ext"
            i=$((i+1))
        done
        printf "   ${CYAN}[%2d]${NC} ${WHITE}Back${NC}\n" "$i"
        echo
        read -r -p "Select script: " sel
        if ! printf "%s" "$sel" | grep -qE '^[0-9]+$'; then echo "Invalid"; continue; fi
        if [ "$sel" -eq "$i" ]; then return; fi
        if [ "$sel" -ge 1 ] && [ "$sel" -lt "$i" ]; then
            run_script "${scripts[$((sel-1))]}"
            echo; read -r -p "Press Enter to continue..."; continue
        else
            echo "Invalid"; continue
        fi
    done
}

# Parse argparse help and prompt per-arg
run_script() {
    local script_path=$1
    local script_name
    script_name=$(basename "$script_path")
    local ext=${script_name##*.}

    echo; echo "Loading: $script_name"; echo

    local help
    if [ "$ext" = "py" ]; then
        help=$($PYTHON_CMD -u "$script_path" --help 2>&1 || true)
    else
        help=$(bash "$script_path" --help 2>&1 || true)
    fi

    if [ -n "$help" ]; then
        echo "---- Help ----"
        printf "%s\n" "$help"
        echo "--------------"
    else
        echo "No help available."; echo
    fi

    # try to extract examples from docstring (python only)
    if [ "$ext" = "py" ]; then
        examples=$(awk 'BEGIN{in=0} NR<=200{ if(in==0 && $0 ~ /"""/){in=1; next} else if(in==1 && $0 ~ /"""/){in=0; exit} else if(in==1){print}}' "$script_path" 2>/dev/null || true)
        if [ -n "$examples" ]; then
            printf "Examples:\n"; printf "%s\n" "$examples" | sed -n '1,8p'; echo
        fi
    fi

    # Extract positional arguments (positional arguments: section preferred)
    pos_section=$(printf "%s\n" "$help" | awk '/^positional arguments:/{flag=1; next} /^optional arguments:/{flag=0} flag')
    pos_args=()
    declare -A pos_desc
    if [ -n "$pos_section" ]; then
        while IFS= read -r line; do
            [ -z "$line" ] && continue
            # skip header lines
            [[ "$line" =~ ^[a-z][a-z\ ]*:$ ]] && continue
            # first token is name
            name=$(printf "%s" "$line" | awk '{print $1}')
            case "$name" in -*) continue ;; esac
            [ -z "$name" ] && continue
            desc=$(printf "%s" "$line" | sed -E 's/^[[:space:]]*[^[:space:]]+[[:space:]]*//')
            pos_args+=("$name")
            pos_desc["$name"]="$desc"
        done < <(printf "%s\n" "$pos_section")
    else
        # fallback: parse usage line for required tokens
        usage_line=$(printf "%s\n" "$help" | grep -i '^usage:' -m1 || true)
        if [ -n "$usage_line" ]; then
            usage_line=$(printf "%s" "$usage_line" | sed -E 's/^[Uu][Ss][Aa][Gg][Ee]: *//')
            usage_line=$(printf "%s" "$usage_line" | awk '{$1=""; sub(/^ /,""); print}')
            for token in $usage_line; do
                case "$token" in -* ) continue ;; esac
                if printf "%s" "$token" | grep -q '^\['; then continue; fi
                clean=$(printf "%s" "$token" | sed -E 's/^\[+//; s/\]+$//')
                [ -n "$clean" ] && pos_args+=("$clean")
            done
        fi
    fi

    # Extract optional arguments
    opt_section=$(printf "%s\n" "$help" | awk '/^optional arguments:/{flag=1; next} flag')
    opt_flags=()
    declare -A opt_needs_val
    declare -A opt_desc
    if [ -n "$opt_section" ]; then
        while IFS= read -r line; do
            # skip header lines and empty lines
            [ -z "$line" ] && continue
            [[ "$line" =~ ^[a-z][a-z\ ]*:$ ]] && continue
            if ! printf "%s" "$line" | grep -qE '^[[:space:]]+-'; then continue; fi
            flags_part=$(printf "%s" "$line" | sed -E 's/[[:space:]]{2,}.*$//')
            IFS=',' read -ra parts <<< "$flags_part"
            long=""; short=""; expects=false
            for p in "${parts[@]}"; do
                pt=$(printf "%s" "$p" | xargs)
                if printf "%s" "$pt" | grep -q -E '=[A-Z]|[[:space:]][A-Z]'; then expects=true; fi
                tok=$(printf "%s" "$pt" | awk '{print $1}')
                if printf "%s" "$tok" | grep -q '^--'; then long="$tok"; elif printf "%s" "$tok" | grep -q '^-' ; then short="$tok"; fi
            done
            pref="$long"; [ -z "$pref" ] && pref="$short"
            if [ -n "$pref" ]; then
                skip=false
                for f in "${opt_flags[@]}"; do [ "$f" = "$pref" ] && skip=true && break; done
                if ! $skip; then
                    opt_flags+=("$pref")
                    opt_needs_val["$pref"]=$expects
                    desc=$(printf "%s" "$line" | sed -E 's/^[[:space:]]*[^[:space:]]+[[:space:]]*//; s/^[[:space:]]*//')
                    opt_desc["$pref"]="$desc"
                fi
            fi
        done < <(printf "%s\n" "$opt_section")
    fi

    # Prompt for positional arguments
    cmd_pos=()
    if [ ${#pos_args[@]} -gt 0 ]; then
        echo
        echo "Provide required values (empty cancels):"
        for p in "${pos_args[@]}"; do
            friendly=$(printf "%s" "$p" | sed -E 's/[^a-zA-Z0-9]+/ /g')
            sample=""
            case "${p,,}" in
                *email*) sample="(e.g. user@example.com)" ;;
                *domain*) sample="(e.g. example.com)" ;;
                *ip*|*addr*) sample="(e.g. 10.0.0.1)" ;;
                *file*|*path*) sample="(e.g. /path/to/file)" ;;
                *port*) sample="(e.g. 80)" ;;
                *url*) sample="(e.g. http://example.com)" ;;
            esac
            desc="${pos_desc[$p]:-}"
            if [ -n "$desc" ]; then
                printf "%s %s - %s\n> " "$friendly" "$sample" "$desc"
            else
                printf "%s %s\n> " "$friendly" "$sample"
            fi
            read -r val
            if [ -z "$val" ]; then echo "Cancelled."; return; fi
            cmd_pos+=("$val")
        done
    fi

    # Prompt for optional flags
    cmd_opts=()
    if [ ${#opt_flags[@]} -gt 0 ]; then
        echo; echo "Optional flags available:"; 
        for opt in "${opt_flags[@]}"; do
            desc="${opt_desc[$opt]:-}"
            if [ -n "$desc" ]; then
                printf "Enable %s - %s ? (y/n): " "$opt" "$desc"
            else
                printf "Enable %s ? (y/n): " "$opt"
            fi
            read -r an
            case "$an" in
                [Yy]* )
                    if [ "${opt_needs_val[$opt]}" = "true" ]; then
                        printf "Enter value for %s: " "$opt"
                        read -r v
                        if [ -n "$v" ]; then cmd_opts+=("$opt" "$v"); else echo "Skipping $opt"; fi
                    else
                        cmd_opts+=("$opt")
                    fi
                    ;;
                * ) ;;
            esac
        done
    fi

    # Build command
    final_cmd=()
    if [ "$ext" = "py" ]; then final_cmd+=("$PYTHON_CMD" -u "$script_path"); else final_cmd+=(bash "$script_path"); fi
    for a in "${cmd_opts[@]}"; do final_cmd+=("$a"); done
    for a in "${cmd_pos[@]}"; do final_cmd+=("$a"); done

    echo; printf "Command to run: %s\n" "${final_cmd[*]}"; read -r -p "Run now? (y/n): " ok
    if [[ "$ok" =~ ^[Yy] ]]; then
        echo
        _run_with_tty "${final_cmd[@]}"
        echo; echo "Execution finished."
    else
        echo "Cancelled."; return
    fi
}

# Main loop
init_script_counts
show_banner
while true; do
    show_main_menu
    read -r -p "Select category: " choice
    case "$choice" in
        1) list_scripts crypto "Crypto" ;; 
        2) list_scripts enumeration "Enumeration" ;; 
        3) list_scripts exploitation "Exploitation" ;; 
        4) list_scripts osint "OSINT" ;; 
        5) list_scripts payloads "Payloads" ;; 
        6) list_scripts scanning "Scanning" ;; 
        7) list_scripts utils "Utils" ;; 
        99) echo -e "${CRIMSON}Goodbye.${NC}"; exit 0 ;;
        *) echo "Invalid selection."; sleep 1 ;;
    esac
done
                    case "$name" in -*) continue ;; esac
