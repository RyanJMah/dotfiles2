source $HOME/custom_aliases.sh

# Load version control information
autoload -Uz vcs_info
precmd() { vcs_info }

# Colors
autoload -U colors && colors
setopt PROMPT_SUBST 

# Prompt layout
PROMPT='%F{cyan}%n%f %F{blue}%~%f %{%F{magenta}%}%b${vcs_info_msg_0_}%{%f%} $ '
