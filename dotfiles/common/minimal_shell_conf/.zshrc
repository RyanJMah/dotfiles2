source $HOME/custom_aliases.sh

source $HOME/.git-prompt.sh

RED="%{$fg[red]%}"
GREEN="%{$fg[green]%}"
YELLOW="%{$fg[yellow]%}"
BLUE="%{$fg[blue]%}"
MAGENTA="%{$fg[magenta]%}"
CYAN="%{$fg[cyan]%}"
WHITE="%{$fg[white]%}"
END="%{$reset_color%}"

setopt PROMPT_SUBST
autoload -U colors && colors
PS1='[%n@%m %c$(__git_ps1 " (%s)")]\$ '
# PS1="${CYAN}%n${END} ${YELLOW}%~${END}${MAGENTA}"$(__git_ps1)"${END} ${GREEN}→${END} "

