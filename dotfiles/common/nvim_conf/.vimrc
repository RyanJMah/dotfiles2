if exists("g:vscode")
	source $HOME/.vscode-vimrc.vim
else
    if has('nvim')
        source $HOME/.terminal-vimrc.vim
    endif
endif
