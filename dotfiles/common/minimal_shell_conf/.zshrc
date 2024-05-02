source $HOME/custom_aliases.sh

source $HOME/git-prompt.sh

RED="%{$fg[red]%}"
GREEN="%{$fg[green]%}"
YELLOW="%{$fg[yellow]%}"
BLUE="%{$fg[blue]%}"
MAGENTA="%{$fg[magenta]%}"
CYAN="%{$fg[cyan]%}"
WHITE="%{$fg[white]%}"
END="%{$reset_color%}"

autoload -U colors && colors
PS1="${CYAN}%n${END} ${YELLOW}%~${END} ${BLUE}git:(${END}${MAGENTA}"$(__git_ps1)"${END}${BLUE})${END} ${GREEN}→${END} "

