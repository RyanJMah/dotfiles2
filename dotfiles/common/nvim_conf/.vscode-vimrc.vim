"-----------------------------------------------------------------------------------
" KEYMAPINGS

nnoremap <silent> dm :delmarks!<CR>

" Ctrl+S to save
noremap  <silent> <C-S> :w<CR>
vnoremap <silent> <C-S> <C-C>:w<CR>
inoremap <silent> <C-S> <C-O>:w<CR>

" Ctrl+Z to undo
nnoremap <C-Z> u
inoremap <C-Z> <Esc>ui

" Ctrl+Y to redo
nnoremap <C-Y> <C-R>
inoremap <C-Y> <Esc><C-R>i

" Alt + Arrows to skip words
nnoremap <A-Left> b
nnoremap <C-Left> b
nnoremap <C-h> b
vnoremap <C-h> b
nnoremap <A-Right> e
nnoremap <C-Right> e
nnoremap <C-l> e
vnoremap <C-l> e

" buffer navigation
nnoremap <silent> bn :bn<CR>
nnoremap <silent> bp :bp<CR>
nnoremap <silent> bd :bd<CR>

" Unmap some stuff cus they're annoying
inoremap <C-A> <NOP>

nnoremap q <NOP>

nnoremap <F2> <NOP>
inoremap <F2> <NOP>
vnoremap <F2> <NOP>

nnoremap <F1> <NOP>
inoremap <F1> <NOP>
vnoremap <F1> <NOP>
"-----------------------------------------------------------------------------------
