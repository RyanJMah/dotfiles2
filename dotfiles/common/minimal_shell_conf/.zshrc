source $HOME/custom_aliases.sh

source $HOME/.git-prompt.sh

autoload -U colors && colors
setopt PROMPT_SUBST

RED="%{$fg[red]%}"
GREEN="%{$fg[green]%}"
YELLOW="%{$fg[yellow]%}"
BLUE="%{$fg[blue]%}"
MAGENTA="%{$fg[magenta]%}"
CYAN="%{$fg[cyan]%}"
WHITE="%{$fg[white]%}"
END="%{$reset_color%}"

PS1='${CYAN}%n${END} ${YELLOW}%~${END}${MAGENTA}$(__git_ps1 " (%s)")${END} ${GREEN}→${END} '
