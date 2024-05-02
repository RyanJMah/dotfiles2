# pretty cat
function pcat() {
    pygmentize -g -O style=native $@
}

# reset cursor
function rc {
    printf "\e[5 q"
}

# shortcut to print github tokens
function github_tokens {
    cat $HOME/main/personal/github_tokens.txt
}

function install_alacritty_terminfo {
    curl -sSL https://raw.githubusercontent.com/alacritty/alacritty/master/extra/alacritty.info | tic -x -
}

# aliases
alias vim="nvim"
alias clear="clear && printf '\e[3J'"

export PATH=$PATH:$HOME/.local/bin
export PATH=$PATH:$HOME/.local/nvim/bin

export PATH=$PATH:$(python3 -c "import site; print(site.USER_BASE + '/bin')")

# source $HOME/platform_custom_aliases.sh

stty -ixon