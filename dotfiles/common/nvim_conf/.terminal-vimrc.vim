" -----------------------------------------------------------------------------------
" GLOBAL SETTINGS

syntax on
set nocompatible
set cursorline
set noerrorbells
set tabstop=4
set softtabstop=4
set sw=4
set expandtab
set smartindent
set nu
set nowrap
set noswapfile
set nobackup
set undodir=~/.vim/undo
set undofile
set incsearch
set hlsearch
set fileformats=unix,dos
set nobinary
set encoding=UTF-8
set formatoptions=jql
set mouse=a
set guicursor+=a:blinkon1
set nomodeline
set nospell

set foldmethod=indent
set foldlevel=1
set foldlevelstart=99
" set foldclose=all

packadd termdebug
" let g:termdebugger="arm-none-eabi-gdb"
let g:termdebugger="gdb"

" detect os and set shell accordingly
let _os = system('if [[ $OSTYPE == "linux-gnu"* ]]; then echo "linux"; else echo "macos"; fi')
if _os == "linux"
    set shell=/bin/zsh
    set g:sh=/bin/zsh
elseif _os == "macos"
    set shell=/usr/bin/zsh
    set g:sh=/usr/bin/zsh
endif

" Use a blinking upright bar cursor in Insert mode, a blinking block in normal
if &term == 'xterm-256color' || &term == 'screen-256color'
    let &t_SI = "\<Esc>[5 q"
    let &t_EI = "\<Esc>[1 q"
endif

" Terminal Function
let g:term_buf = 0
let g:term_win = 0
function! TermToggle(height)
    if win_gotoid(g:term_win)
        hide
    else
        botright new
        exec "resize" . a:height
        " botright vs new
        " vertical resize 55
        try
            exec "buffer " . g:term_buf
        catch
            call termopen($SHELL)
            " let g:term_buf = bufnr("")
            set nonumber
            " set norelativenumber
            " set signcolumn=no
        endtry
        startinsert!
        let g:term_win = win_getid()
    endif
endfunction

" close buffer wihtout closing pane
" Delete buffer while keeping window layout (don't close buffer's windows).
" Version 2008-11-18 from http://vim.wikia.com/wiki/VimTip165
if v:version < 700 || exists('loaded_bclose') || &cp
  finish
endif
let loaded_bclose = 1
if !exists('bclose_multiple')
  let bclose_multiple = 1
endif

" Display an error message.
function! s:Warn(msg)
  echohl ErrorMsg
  echomsg a:msg
  echohl NONE
endfunction

" Command ':Bclose' executes ':bd' to delete buffer in current window.
" The window will show the alternate buffer (Ctrl-^) if it exists,
" or the previous buffer (:bp), or a blank buffer if no previous.
" Command ':Bclose!' is the same, but executes ':bd!' (discard changes).
" An optional argument can specify which buffer to close (name or number).
function! s:Bclose(bang, buffer)
    if empty(a:buffer)
        let btarget = bufnr('%')
    elseif a:buffer =~ '^\d\+$'
        let btarget = bufnr(str2nr(a:buffer))
    else
        let btarget = bufnr(a:buffer)
    endif
    if btarget < 0
        call s:Warn('No matching buffer for '.a:buffer)
        return
    endif
    if empty(a:bang) && getbufvar(btarget, '&modified')
        call s:Warn('No write since last change for buffer '.btarget.' (use :Bclose!)')
        return
    endif
    " Numbers of windows that view target buffer which we will delete.
    let wnums = filter(range(1, winnr('$')), 'winbufnr(v:val) == btarget')
    if !g:bclose_multiple && len(wnums) > 1
        call s:Warn('Buffer is in multiple windows (use ":let bclose_multiple=1")')
        return
    endif
    let wcurrent = winnr()
    for w in wnums
        execute w.'wincmd w'
        let prevbuf = bufnr('#')
        if prevbuf > 0 && buflisted(prevbuf) && prevbuf != btarget
            buffer #
        else
            BufferLineCycleNext
        endif
        if btarget == bufnr('%')
            " Numbers of listed buffers which are not the target to be deleted.
            let blisted = filter(range(1, bufnr('$')), 'buflisted(v:val) && v:val != btarget')
            " Listed, not target, and not displayed.
            let bhidden = filter(copy(blisted), 'bufwinnr(v:val) < 0')
            " Take the first buffer, if any (could be more intelligent).
            let bjump = (bhidden + blisted + [-1])[0]
            if bjump > 0
                execute 'buffer '.bjump
            else
                execute 'enew'.a:bang
            endif
        endif
    endfor
    execute 'bdelete'.a:bang.' '.btarget
    execute wcurrent.'wincmd w'
endfunction
command! -bang -complete=buffer -nargs=? Bclose call <SID>Bclose(<q-bang>, <q-args>)
nnoremap <silent> <Leader>bd :Bclose<CR>

"-----------------------------------------------------------------------------------

"-----------------------------------------------------------------------------------
" KEYMAPINGS

nnoremap <silent> md :delmarks!<CR>

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
nnoremap <silent> bn :BufferLineCycleNext<CR>
nnoremap <silent> bp :BufferLineCyclePrev<CR>
nnoremap <silent> bd :Bclose<CR>


" comment out line
nnoremap <silent> <C-/> :Commentary<CR>
vnoremap <silent> <C-/> :Commentary<CR>
inoremap <silent> <C-/> <C-O>:Commentary<CR>

nnoremap <silent> <C-_> :Commentary<CR>
vnoremap <silent> <C-_> :Commentary<CR>
inoremap <silent> <C-_> <C-O>:Commentary<CR>

" searching
nnoremap <C-p> :Telescope find_files hidden=true<CR>
command! Search :Telescope live_grep

" Open terminal
command! NewTerm :call termopen($SHELL)

" Alt+t to toggle terminal
nnoremap <silent> <A-t> :call TermToggle(9)<CR>
tnoremap <silent> <A-t> <C-\><C-n>:call TermToggle(9)<CR>

tnoremap <silent> <Esc> <C-\><C-n>

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

"-----------------------------------------------------------------------------------
" COLOR SCHEME

set termguicolors
let g:sonokai_style = 'dark'
let g:sonokai_style = 'darker'
let g:airline_theme = 'sonokai'
let g:sonokai_disable_italic_comment = 0
let g:sonokai_enable_italic = 1
colorscheme sonokai
"-----------------------------------------------------------------------------------

"-----------------------------------------------------------------------------------
" TERMDEBUG SETTINGS
let g:termdebug_wide=1
"-----------------------------------------------------------------------------------

"-----------------------------------------------------------------------------------
" WINDOW RESIZING
let g:winresizer_start_key = "<C-R>"
let g:winresizer_vert_resize = 4
let g:winresizer_horiz_resize = 1
"-----------------------------------------------------------------------------------


"-----------------------------------------------------------------------------------
" Autocomplete
lua <<EOF
    -- Set up nvim-cmp.
    local cmp = require'cmp'

    cmp.setup({
        snippet = {
            -- REQUIRED - you must specify a snippet engine
            expand = function(args)
                vim.fn["vsnip#anonymous"](args.body) -- For `vsnip` users.
                -- require('luasnip').lsp_expand(args.body) -- For `luasnip` users.
                -- require('snippy').expand_snippet(args.body) -- For `snippy` users.
                -- vim.fn["UltiSnips#Anon"](args.body) -- For `ultisnips` users.
                -- vim.snippet.expand(args.body) -- For native neovim snippets (Neovim v0.10+)
            end,
        },
        window = {
            -- completion = cmp.config.window.bordered(),
            -- documentation = cmp.config.window.bordered(),
        },
        mapping = cmp.mapping.preset.insert({
            ["<Tab>"] = cmp.mapping(function(fallback)
                if cmp.visible() then
                    cmp.select_next_item()
                else
                    fallback()
                end
            end, {"i", "s"}),

            ["<S-Tab>"] = cmp.mapping(function(fallback)
                if cmp.visible() then
                    cmp.select_prev_item()
                else
                    fallback()
                end
            end, {"i", "s"}),

            ['<CR>'] = cmp.mapping.confirm({ select = true }),

            ['<C-b>'] = cmp.mapping.scroll_docs(-4),
            ['<C-f>'] = cmp.mapping.scroll_docs(4),
        }),
        sources = cmp.config.sources({
            { name = 'nvim_lsp' },
            { name = 'vsnip' }, -- For vsnip users.
            -- { name = 'luasnip' }, -- For luasnip users.
            -- { name = 'ultisnips' }, -- For ultisnips users.
            -- { name = 'snippy' }, -- For snippy users.
        },
        {
            { name = 'buffer' },
        })
    })
    -- Use buffer source for `/` and `?` (if you enabled `native_menu`, this won't work anymore).
    cmp.setup.cmdline({ '/', '?' }, {
        mapping = cmp.mapping.preset.cmdline(),
        sources = {
            { name = 'buffer' }
        }
    })

    -- Use cmdline & path source for ':' (if you enabled `native_menu`, this won't work anymore).
    cmp.setup.cmdline(':', {
        mapping = cmp.mapping.preset.cmdline(),
        sources = cmp.config.sources({
            { name = 'path' }
        }),
        matching = { disallow_symbol_nonprefix_matching = false }
    })

    -- Set up lspconfig.
    local capabilities = require('cmp_nvim_lsp').default_capabilities()
EOF
"-----------------------------------------------------------------------------------

"-----------------------------------------------------------------------------------
" Treesitter
lua << EOF
require("nvim-autopairs").setup {}

require'nvim-treesitter.configs'.setup {
    ensure_installed = {
        "vim",
        "lua",
        "c",
        "cpp",
        "make",
        "cmake",
        "devicetree",
        "python",
        "matlab",
        "dockerfile",
        "json",
        "jsonc",
        "verilog",
        "gitcommit",
        "gitignore"
    },

    highlight = {
        enable = true,
    },

    sync_install = false,
}
EOF
""-----------------------------------------------------------------------------------

"-----------------------------------------------------------------------------------
" File explorer

nmap <silent> <C-B> :silent NvimTreeToggle<CR>

let g:loaded_netrw = 1
let g:loaded_netrwPlugin = 1

lua << EOF

-- bruh this is so fucking stupid
local function on_attach(bufnr)
    local api = require('nvim-tree.api')
    
    local function opts(desc)
        return { desc = 'nvim-tree: ' .. desc, buffer = bufnr, noremap = true, silent = true, nowait = true }
    end
    
    
    -- Default mappings. Feel free to modify or remove as you wish.
    --
    -- BEGIN_DEFAULT_ON_ATTACH
    vim.keymap.set('n', '<C-]>', api.tree.change_root_to_node,          opts('CD'))
    vim.keymap.set('n', '<C-e>', api.node.open.replace_tree_buffer,     opts('Open: In Place'))
    vim.keymap.set('n', '<C-k>', api.node.show_info_popup,              opts('Info'))
    vim.keymap.set('n', '<C-r>', api.fs.rename_sub,                     opts('Rename: Omit Filename'))
    vim.keymap.set('n', '<C-t>', api.node.open.tab,                     opts('Open: New Tab'))
    vim.keymap.set('n', '<C-v>', api.node.open.vertical,                opts('Open: Vertical Split'))
    vim.keymap.set('n', '<C-x>', api.node.open.horizontal,              opts('Open: Horizontal Split'))
    vim.keymap.set('n', '<BS>',  api.node.navigate.parent_close,        opts('Close Directory'))
    vim.keymap.set('n', '<CR>',  api.node.open.edit,                    opts('Open'))
    vim.keymap.set('n', '<Tab>', api.node.open.preview,                 opts('Open Preview'))
    vim.keymap.set('n', '>',     api.node.navigate.sibling.next,        opts('Next Sibling'))
    vim.keymap.set('n', '<',     api.node.navigate.sibling.prev,        opts('Previous Sibling'))
    vim.keymap.set('n', '.',     api.node.run.cmd,                      opts('Run Command'))
    vim.keymap.set('n', '-',     api.tree.change_root_to_parent,        opts('Up'))
    vim.keymap.set('n', 'a',     api.fs.create,                         opts('Create'))
    vim.keymap.set('n', 'bmv',   api.marks.bulk.move,                   opts('Move Bookmarked'))
    vim.keymap.set('n', 'B',     api.tree.toggle_no_buffer_filter,      opts('Toggle No Buffer'))
    vim.keymap.set('n', 'c',     api.fs.copy.node,                      opts('Copy'))
    vim.keymap.set('n', 'C',     api.tree.toggle_git_clean_filter,      opts('Toggle Git Clean'))
    vim.keymap.set('n', '[c',    api.node.navigate.git.prev,            opts('Prev Git'))
    vim.keymap.set('n', ']c',    api.node.navigate.git.next,            opts('Next Git'))
    vim.keymap.set('n', 'd',     api.fs.remove,                         opts('Delete'))
    vim.keymap.set('n', 'D',     api.fs.trash,                          opts('Trash'))
    vim.keymap.set('n', 'E',     api.tree.expand_all,                   opts('Expand All'))
    vim.keymap.set('n', 'e',     api.fs.rename_basename,                opts('Rename: Basename'))
    vim.keymap.set('n', ']e',    api.node.navigate.diagnostics.next,    opts('Next Diagnostic'))
    vim.keymap.set('n', '[e',    api.node.navigate.diagnostics.prev,    opts('Prev Diagnostic'))
    vim.keymap.set('n', 'F',     api.live_filter.clear,                 opts('Clean Filter'))
    vim.keymap.set('n', 'f',     api.live_filter.start,                 opts('Filter'))
    vim.keymap.set('n', 'g?',    api.tree.toggle_help,                  opts('Help'))
    vim.keymap.set('n', 'gy',    api.fs.copy.absolute_path,             opts('Copy Absolute Path'))
    vim.keymap.set('n', 'H',     api.tree.toggle_hidden_filter,         opts('Toggle Dotfiles'))
    vim.keymap.set('n', 'I',     api.tree.toggle_gitignore_filter,      opts('Toggle Git Ignore'))
    vim.keymap.set('n', 'J',     api.node.navigate.sibling.last,        opts('Last Sibling'))
    vim.keymap.set('n', 'K',     api.node.navigate.sibling.first,       opts('First Sibling'))
    vim.keymap.set('n', 'm',     api.marks.toggle,                      opts('Toggle Bookmark'))
    vim.keymap.set('n', 'o',     api.node.open.edit,                    opts('Open'))
    vim.keymap.set('n', 'O',     api.node.open.no_window_picker,        opts('Open: No Window Picker'))
    vim.keymap.set('n', 'p',     api.fs.paste,                          opts('Paste'))
    vim.keymap.set('n', 'P',     api.node.navigate.parent,              opts('Parent Directory'))
    vim.keymap.set('n', 'q',     api.tree.close,                        opts('Close'))
    vim.keymap.set('n', 'r',     api.fs.rename,                         opts('Rename'))
    vim.keymap.set('n', 'R',     api.tree.reload,                       opts('Refresh'))
    vim.keymap.set('n', 's',     api.node.run.system,                   opts('Run System'))
    vim.keymap.set('n', 'S',     api.tree.search_node,                  opts('Search'))
    vim.keymap.set('n', 'U',     api.tree.toggle_custom_filter,         opts('Toggle Hidden'))
    vim.keymap.set('n', 'W',     api.tree.collapse_all,                 opts('Collapse'))
    vim.keymap.set('n', 'x',     api.fs.cut,                            opts('Cut'))
    vim.keymap.set('n', 'y',     api.fs.copy.filename,                  opts('Copy Name'))
    vim.keymap.set('n', 'Y',     api.fs.copy.relative_path,             opts('Copy Relative Path'))
    vim.keymap.set('n', '<2-LeftMouse>',  api.node.open.edit,           opts('Open'))
    vim.keymap.set('n', '<2-RightMouse>', api.tree.change_root_to_node, opts('CD'))
    -- END_DEFAULT_ON_ATTACH
    
    
    -- Mappings removed via:
    --   remove_keymaps
    --   OR
    --   view.mappings.list..action = ""
    --
    -- The dummy set before del is done for safety, in case a default mapping does not exist.
    --
    -- You might tidy things by removing these along with their default mapping.
    vim.keymap.set('n', '<C-R>', '', { buffer = bufnr })
    vim.keymap.del('n', '<C-R>', { buffer = bufnr })
end

require("nvim-tree").setup({
    sort_by = "extension",
    actions = {
        open_file = {
            quit_on_open = true
        }
    },
    on_attach = on_attach,
    git = {
        ignore = false,
    },
    filters = {
        custom = {".DS_Store"}
    },
    view = {
        preserve_window_proportions = true
    },
    diagnostics = {
        enable = false
    }
})

require'nvim-web-devicons'.setup {}

local git_icon = ""
local git_color = "#f1502f"
local md_icon = ""
local md_color = "#F09F17"

require("nvim-web-devicons").set_icon {
    gitattributes = {
        icon = git_icon,
        color = git_color,
        name = "GitAttributes"
    },
    gitignore = {
        icon = git_icon,
        color = git_color,
        name = "GitIgnore"
    },
    gitmodules = {
        icon = git_icon,
        color = git_color,
        name = "GitModules"
    },

    markdown = {
        icon = md_icon,
        color = md_color,
        name = "Markdown"
    },
    md = {
        icon = md_icon,
        color = md_color,
        name = "Md"
    },

    txt = {
        icon = "",
        color = "#519aba",
        name = "Txt"
    }
}
EOF

autocmd Filetype NvimTree setlocal sw=2
"-----------------------------------------------------------------------------------

"-----------------------------------------------------------------------------------
" gitgutter

let g:gitgutter_sign_added = '│'
let g:gitgutter_sign_modified = '│'
let g:gitgutter_sign_removed = ''
let g:gitgutter_sign_removed_first_line = '-'
let g:gitgutter_sign_removed_above_and_below = '-'
let g:gitgutter_sign_modified_removed = '~'
"-----------------------------------------------------------------------------------

"-----------------------------------------------------------------------------------
" Buffer tabs
lua << EOF
local configuration = vim.fn['sonokai#get_configuration']()
local p = vim.fn['sonokai#get_palette'](configuration.style, configuration.colors_override)

-- lua arrays start a 1 for some reaason
fg        = p.fg[1]
bg0       = p.bg0[1]
bg3       = p.bg3[1]
bg_red    = p.bg_red[1]
darker_bg = p.darker_bg[1]
bg_green  = p.bg_green[1]

local bufferline = require("bufferline")

bufferline.setup{
    options = {
        separator_style = "thin",
        -- enfore_regular_tabs = false,
        truncate_names = false,
        -- tab_size = 15
    },
    highlights = {
        fill = {
            fg = fg,
            bg = darker_bg
        },
        buffer_selected = {
            italic = false,
            bold = false,
            bg = bg0,
            fg = fg
        }
        -- buffer_selected = {
        --     fg = bg_red,
        --     bg = bg0
        -- }
    }
}
EOF

"-----------------------------------------------------------------------------------

"-----------------------------------------------------------------------------------
" STATUSLINE
" let g:airline_powerline_fonts = 1

let g:airline#extensions#tabline#enabled = 0
let g:airline#extensions#tabline#alt_sep = 0
let g:airline#extensions#tabline#right_sep = ''
let g:airline#extensions#tabline#right_alt_sep = ''
let g:airline#extensions#branch#enabled = 1
let g:airline#extensions#hunks#enabled = 0

if !exists('g:airline_symbols')
  let g:airline_symbols = {}
endif

" unicode symbols
let g:airline_symbols.crypt = '🔒'
let g:airline_symbols.paste = 'ρ'
let g:airline_symbols.paste = 'Þ'
let g:airline_symbols.paste = '∥'
let g:airline_symbols.spell = 'Ꞩ'
let g:airline_symbols.notexists = 'Ɇ'
let g:airline_symbols.whitespace = 'Ξ'" let g:airline#extensions#tabline#formatter = 'unique_tail'

let g:airline_left_sep = ''
let g:airline_left_alt_sep = ''
let g:airline_right_sep = ''
let g:airline_right_alt_sep = ''

" let g:airline_left_sep = ''
" let g:airline_left_alt_sep = ''
" let g:airline_right_sep = ''
" let g:airline_right_alt_sep = ''
let g:airline_symbols.branch = ''
let g:airline_symbols.readonly = ''
" let g:airline_symbols.colnr = ' :'
" let g:airline_symbols.linenr = ' :'
let g:airline_symbols.colnr = 'CN:'
let g:airline_symbols.linenr = ' LN:'
let g:airline_symbols.maxlinenr = ' '
let g:airline_symbols.dirty=''

let g:airline#extensions#tabline#ignore_bufadd_pat = 'defx|gundo|nerd_tree|startify|tagbar|undotree|vimfiler'

let g:airline_filetype_overrides = {
    \ 'NvimTree': [ "NvimTree", '' ]
\ }
"-----------------------------------------------------------------------------------

"-----------------------------------------------------------------------------------
" indent blankline
lua <<EOF
require("ibl").setup {
    indent = {
        char = '│',
    },
    scope = {
        enabled = false
    }
}
EOF
"-----------------------------------------------------------------------------------

"-----------------------------------------------------------------------------------
" Commentary
autocmd Filetype c setlocal commentstring=//\ %s
autocmd Filetype cpp setlocal commentstring=//\ %s
autocmd Filetype verilog setlocal commentstring=//\ %s
"-----------------------------------------------------------------------------------

"-----------------------------------------------------------------------------------
" More color stuff

lua << EOF
local configuration = vim.fn['sonokai#get_configuration']()
local p = vim.fn['sonokai#get_palette'](configuration.style, configuration.colors_override)
local apply_hl = vim.fn["sonokai#highlight"]

apply_hl("TelescopeBorder", p.darker_bg, p.darker_bg)
apply_hl("TelescopePromptBorder", p.bg1, p.bg1)
apply_hl("TelescopePromptCounter", p.grey, p.bg1)
apply_hl("TelescopePromptNormal", p.fg, p.bg1)
apply_hl("TelescopePromptPrefix", p.bg_red, p.bg1)
apply_hl("TelescopeNormal", p.none, p.darker_bg)
apply_hl("TelescopePreviewTitle", p.bg0, p.bg_green)
apply_hl("TelescopePromptTitle", p.bg0, p.bg_red)
apply_hl("TelescopeResultsTitle", p.darker_bg, p.darker_bg)
apply_hl("TelescopeSelection", p.fg, p.bg1)
apply_hl("TelescopeResultsDiffAdd", p.bg_green, p.none)
apply_hl("TelescopeResultsDiffChange", p.yellow, p.none)
apply_hl("TelescopeResultsDiffDelete", p.bg_red, p.none)

local options = {
    defaults = {
        prompt_prefix = "    ",
        initial_mode = "insert",
        selection_strategy = "reset",
        sorting_strategy = "ascending",
        layout_strategy = "horizontal",
        layout_config = {
            horizontal = {
                prompt_position = "top",
                preview_width = 0.55,
                results_width = 0.8,
            },
            vertical = {
                mirror = false,
            },
            width = 0.87,
            height = 0.80,
        },
    },
    extensions_list = { "themes", "terms" },
}

require("telescope").setup(options)
EOF
"-----------------------------------------------------------------------------------

"-----------------------------------------------------------------------------------
" hex editor
lua << EOF
require 'hex'.setup()
EOF
"-----------------------------------------------------------------------------------

" "-----------------------------------------------------------------------------------

autocmd BufWinEnter,BufNewFile,BufRead,VimEnter,FileType,OptionSet * set formatoptions=jql
autocmd BufWinEnter,BufNewFile,BufRead,VimEnter,FileType,OptionSet * setlocal formatoptions=jql
" autocmd BufReadPost,OptionSet * silent :GuessIndent

autocmd BufRead,BufNewFile project/*.c setlocal formatoptions-=cro

autocmd VimLeave,VimLeavePre * :set guicursor=n:ver100-iCursor

autocmd FileChangedRO * echohl WarningMsg | echo "File changed RO." | echohl None
autocmd FileChangedShell * echohl WarningMsg | echo "File changed shell." | echohl None

autocmd BufWinEnter,WinEnter term://* startinsert
autocmd TermOpen * setlocal nonumber norelativenumber
autocmd TermOpen * if bufwinnr('') > 0 | setlocal nobuflisted | endif
autocmd TermClose * setlocal number | :Bclose!
