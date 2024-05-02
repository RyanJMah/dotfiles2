source $HOME/custom_aliases.sh

# Custom prompt with color-changing arrow based on exit status
set_prompt(){
    local arrow_color="%F{green}"
    if [ $? -ne 0 ]; then
        arrow_color="%F{red}"
    fi

    # Set the prompt
    PROMPT="%F{cyan}%n %F{240}%~ %F{yellow}git:(%F{magenta}%b%f)%F{white} ➜ $arrow_color"
}

# Tell zsh to use this function to set the prompt
autoload -Uz add-zsh-hook
add-zsh-hook precmd set_prompt

# Reset color for command output
autoload -U colors && colors
