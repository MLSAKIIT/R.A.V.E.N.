#!/bin/bash

# R.A.V.E.N - Rapid Automation & Vulnerability Enumeration for Networks
# Bash CLI Interface
# Version: 1.0.4 (Robust tty redirection)

# -------------------------
# Color definitions
# -------------------------
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

# ensure Python unbuffered
export PYTHONUNBUFFERED=1

# -------------------------
# Banner
# -------------------------
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

# -------------------------
# Script counters
# -------------------------
declare -A script_counts
init_script_counts() {
    local categories=("crypto" "enumeration" "exploitation" "osint" "payloads" "scanning" "utils")
    for category in "${categories[@]}"; do
        if [[ -d "scripts/$category" ]]; then
            script_counts["$category"]=$(find "scripts/$category" -type f \( -name "*.py" -o -name "*.sh" \) 2>/dev/null | wc -l)
        else
            script_counts["$category"]=0
        fi
    done
}

get_script_count() {
    local category=$1
    echo "${script_counts[$category]:-0}"
}

# -------------------------
# Menu display
# -------------------------
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

# -------------------------
# List scripts
# -------------------------
list_scripts() {
    local category=$1
    local category_name=$2
    if [[ ! -d "scripts/$category" ]]; then
        echo
        echo -e "                        ${BRIGHT_RED}⟨ ${category_name^^} MODULE ⟩${NC}"
        echo
        echo -e "   ${ROYAL_BLUE}◇ NO EXPLOITS LOADED IN THIS MODULE${NC}"
        echo -e "   ${ROYAL_BLUE}◇ AWAITING CONTRIBUTION...${NC}"
        echo -e "   ${ROYAL_BLUE}◇ CHECK CONTRIBUTING.md FOR DEPLOYMENT GUIDE${NC}"
        echo
        echo -ne "${CRIMSON}▶ Press ENTER to return to main menu...${NC}"
        read -r
        return 1
    fi

    mapfile -t scripts < <(find "scripts/$category" -type f \( -name "*.py" -o -name "*.sh" \) 2>/dev/null | sort)
    if [[ ${#scripts[@]} -eq 0 ]]; then
        echo
        echo -e "                        ${BRIGHT_RED}⟨ ${category_name^^} MODULE ⟩${NC}"
        echo
        echo -e "   ${ROYAL_BLUE}◇ NO EXPLOITS LOADED IN THIS MODULE${NC}"
        echo -e "   ${ROYAL_BLUE}◇ AWAITING CONTRIBUTION...${NC}"
        echo -e "   ${ROYAL_BLUE}◇ CHECK CONTRIBUTING.md FOR DEPLOYMENT GUIDE${NC}"
        echo
        echo -ne "${CRIMSON}▶ Press ENTER to return to main menu...${NC}"
        read -r
        return 1
    fi

    echo
    echo -e "                        ${BRIGHT_RED}⟨ ${category_name^^} ARSENAL ⟩${NC}"
    echo

    for i in "${!scripts[@]}"; do
        script_path="${scripts[i]}"
        script_name=$(basename "$script_path")
        script_folder=$(basename "$(dirname "$script_path")")
        script_ext="${script_name##*.}"
        script_type="⟨${script_ext^^}⟩"
        printf "   ${ROYAL_BLUE}[%2s]${NC} ${WHITE}%-30s${NC} ${CYAN}/ %-15s${NC} ${CRIMSON}%s${NC}\n" "$((i+1))" "$script_folder" "$script_name" "$script_type"
    done

    echo
    printf "   ${BRIGHT_RED}[%2s] ⟨ BACK TO MAIN MENU ⟩${NC}\n" "$((${#scripts[@]}+1))"

    while true; do
        echo
        echo -ne "${CRIMSON}▶ SELECT EXPLOIT: ${NC}"
        read -r choice
        if [[ "$choice" == "$((${#scripts[@]}+1))" ]]; then
            return 1
        elif [[ "$choice" =~ ^[0-9]+$ ]] && [[ "$choice" -ge 1 ]] && [[ "$choice" -le ${#scripts[@]} ]]; then
            run_script "${scripts[$((choice-1))]}"
            echo -ne "\n${CRIMSON}▶ Press ENTER to continue...${NC}"
            read -r
            list_scripts "$category" "$category_name"
            return
        else
            echo -e "${BRIGHT_RED}  [!] Invalid selection. Try again.${NC}"
        fi
    done
}

# -------------------------
# Robust function to run processes with real tty mapped
# -------------------------
_run_with_tty() {
    # usage: _run_with_tty <command> [args...]
    # maps stdin/out/err to the controlling tty if available
    local cmd=("$@")
    local ttydev
    ttydev=$(tty 2>/dev/null) || ttydev=""

    if [[ -n "$ttydev" && -c "$ttydev" ]]; then
        # preserve term state
        local sttystate
        sttystate=$(stty -g 2>/dev/null) || sttystate=""
        stty sane 2>/dev/null || true

        # run with stdin/stdout/stderr attached to the tty device
        "${cmd[@]}" <"$ttydev" >"$ttydev" 2>"$ttydev"
        local rc=$?

        # restore stty
        if [[ -n "$sttystate" ]]; then
            stty "$sttystate" 2>/dev/null || true
        else
            stty sane 2>/dev/null || true
        fi

        return $rc
    else
        # fallback: run normally
        "${cmd[@]}"
        return $?
    fi
}

# -------------------------
# Run script: show help & execute
# -------------------------
run_script() {
    local script_path=$1
    local script_name
    script_name=$(basename "$script_path")
    local script_ext="${script_name##*.}"

    echo
    echo -e "                        ${BRIGHT_RED}⟨ LOADING EXPLOIT ⟩${NC}"
    echo
    echo -e "   ${ROYAL_BLUE}◆ SCRIPT:${NC} ${WHITE}${script_name}${NC}"
    echo

    if [[ "$script_ext" == "py" ]]; then
        echo -e "${ROYAL_BLUE}▶ Displaying Python script help:${NC}"
        _run_with_tty python3 -u "$script_path" --help 2>/dev/null || echo -e "${BRIGHT_RED}◇ No help available for this script${NC}"
    elif [[ "$script_ext" == "sh" ]]; then
        echo -e "${ROYAL_BLUE}▶ Displaying Shell script help:${NC}"
        bash "$script_path" --help 2>/dev/null || echo -e "${BRIGHT_RED}◇ No help available for this script${NC}"
    fi

    echo
    echo -ne "${BRIGHT_RED}Execute with custom arguments? (y/N): ${NC}"
    read -r execute_choice
    if [[ "$execute_choice" =~ ^[Yy]$ ]]; then
        echo -ne "${BRIGHT_RED}▶ Enter arguments: ${NC}"
        IFS= read -r args_line
        read -r -a args_array <<< "$args_line"
        echo

        echo -e "                        ${BRIGHT_RED}⟨ EXECUTING EXPLOIT ⟩${NC}"
        echo

        if [[ "$script_ext" == "py" ]]; then
            # run python with stdout/stderr/stdin attached to tty
            _run_with_tty python3 -u "$script_path" "${args_array[@]}"
        else
            _run_with_tty bash "$script_path" "${args_array[@]}"
        fi

        echo
        echo -e "                      ${ROYAL_BLUE}⟨ EXECUTION COMPLETED ⟩${NC}"
    else
        echo -e "${ROYAL_BLUE}▶ Execution cancelled${NC}"
    fi
}

# -------------------------
# Main program
# -------------------------
main() {
    if [[ ! -d "scripts" ]]; then
        echo -e "${BRIGHT_RED}Error: scripts directory not found. Please run from R.A.V.E.N root directory.${NC}"
        exit 1
    fi

    echo -e "${ROYAL_BLUE}▶ Initializing R.A.V.E.N interface...${NC}"
    init_script_counts

    declare -A category_map=(
        ["1"]="crypto:🔐 Cryptographic Tools"
        ["2"]="enumeration:📊 Service Enumeration Tools"
        ["3"]="exploitation:💥 Exploit Tools and Payloads"
        ["4"]="osint:🕵️ Open Source Intelligence"
        ["5"]="payloads:🎯 Payload Generators"
        ["6"]="scanning:🔍 Port Scanning and Service Detection"
        ["7"]="utils:🔧 General Utility Scripts"
    )

    while true; do
        show_banner
        show_main_menu
        echo
        echo -ne "${BRIGHT_RED}▶ SELECT TARGET: ${NC}"
        read -r choice
        if [[ "$choice" == "99" ]]; then
            echo -e "\n${BRIGHT_RED}  ► SESSION TERMINATED"
            echo -e "  ► REMEMBER: USE ETHICALLY & LEGALLY ONLY"
            echo -e "  ► STAY SECURE, HACKER! ${NC}"
            exit 0
        elif [[ -n "${category_map[$choice]}" ]]; then
            IFS=':' read -r folder description <<< "${category_map[$choice]}"
            clear
            show_banner
            list_scripts "$folder" "$description"
        else
            echo -e "${BRIGHT_RED}  [!] Invalid selection. Try again.${NC}"
            sleep 0.5
        fi
    done
}

# ensure terminal restored on Ctrl-C
trap 'echo -e "\n${BRIGHT_RED}  ► SESSION TERMINATED BY USER${NC}"; stty sane 2>/dev/null || true; exit 0' INT

main "$@"
