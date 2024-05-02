source $HOME/custom_aliases.sh

source $HOME/.git-prompt.sh

autoload -U colors && colors
setopt PROMPT_SUBST
PS1='%{$fg[cyan]%}%n%{$reset_color%} %{$fg[yellow]%}%~%{$reset_color%}%{$fg[blue]%}$(__git_ps1 " git:(%%{$reset_color%%}%%{$fg[magenta]%%}%s%%{$reset_color%%}%%{$fg[blue]%%})")%{$reset_color%} %{$fg[green]%}→%{$reset_color%} '
