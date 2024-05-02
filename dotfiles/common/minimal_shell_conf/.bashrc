# Source external scripts
source $HOME/custom_aliases.sh
source $HOME/.git-prompt.sh

# Function to determine color based on exit status
prompt_status() {
    if [ $? -eq 0 ]; then
        echo -ne "\[\033[1;32m\]"  # Green
    else
        echo -ne "\[\033[1;31m\]"  # Red
    fi
}

# Customize the PS1 variable to define your prompt
PS1='\[\033[0;36m\]\u\[\033[00m\] \[\033[0;33m\]\w\[\033[00m\]$(git branch 2>/dev/null | grep '^*' | colrm 1 2 | xargs -I {} echo "\[\033[0;34m\] git:(\[\033[00m\]\[\033[0;35m\]{}{}\[\033[00m\]\[\033[0;34m\])")\[\033[00m\] $(prompt_status)→\[\033[00m\] '

# Enable color support of ls and also add handy aliases
alias ls='ls --color=auto'
