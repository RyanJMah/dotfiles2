source $HOME/.custom_aliases.sh
source $HOME/.git-prompt.sh

autoload -U colors && colors
setopt PROMPT_SUBST

# Function to determine color based on exit status
prompt_status() {
    if [[ $? -eq 0 ]]; then
        echo "%{$fg_bold[green]%}"
    else
        echo "%{$fg_bold[red]%}"
    fi
}

PS1='%{$fg[cyan]%}%n%{$reset_color%} %{$fg[yellow]%}%~%{$reset_color%}%{$fg[blue]%}$(__git_ps1 " git:(%%{$reset_color%%}%%{$fg[magenta]%%}%s%%{$reset_color%%}%%{$fg[blue]%%})")%{$reset_color%} $(prompt_status)→%{$reset_color%} '
