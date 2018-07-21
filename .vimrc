runtime bundle/vim-pathogen/autoload/pathogen.vim
execute pathogen#infect()

if has('win32') || has('win64')
   set runtimepath=$HOME/.vim,$VIM/vimfiles,$VIMRUNTIME,$VIM/vimfiles/after,$HOME/.vim/after
   set lines=100 columns=100
   let MRU_File = $USERPROFILE . "/.vim_mru_files"
   let g:indexer_indexerListFilename = $USERPROFILE . "/.indexer_files"
else
   let g:MRU_File = $HOME . "/.vim_mru_files"
   let g:indexer_indexerListFilename = $HOME . "/.indexer_files"
endif

syn on
set hidden
set history=2000
set expandtab
set shellslash
colorscheme wombat256
set nowrap
set hls
if has("unix")
   set guifont=Monospace
else
   set guifont=Consolas
endif
set ignorecase
set smartcase
set scrolloff=2
set wildmode=longest,list
set incsearch
set smarttab
set bs=2
filetype plugin indent on

let g:ctrlp_max_height = 20
let g:ctrlp_regexp = 1
let g:ctrlp_working_path_mode = 0
let g:ctrlp_mruf_relative = 1
let g:ctrlp_max_files = 0
let g:ctrlp_custom_ignore = {
   \ 'dir':  '\.repo$\|\.git$\|\.hg$\|\.svn$\|target$',
   \ 'file': '\.pyc$\|\.class$\|\.swp$\|\.P$\|\.o$\|\.exe$\|\.so$\|\.dll$\|\.DS_Store$',
   \ 'link': 'SOME_BAD_SYMBOLIC_LINKS',
   \ }

" Re-map leader modifier to ','
let mapleader = ","

" Show whitespace
"set listchars=tab:>-,trail:·,eol:$
nmap <silent> <leader>s :set nolist!<CR>

" Turn off search temporarily
nmap <silent> <leader>n :silent :nohlsearch<CR>

" tell VIM to always put a status line in, even if there is only one window
set laststatus=2

" Set the status line
set stl=%f\ %m\ Line:%l/%L[%p%%]\ Col:%v\ Buf:#%n\ [%b][0x%B]

nnoremap <C-H> :Hexmode<CR>
inoremap <C-H> <Esc>:Hexmode<CR>
vnoremap <C-H> :<C-U>Hexmode<CR>

map <F4> :execute "vimgrep /" . expand("<cword>") . "/j **" <Bar> cw<CR>
map <F3> :execute "! ack /" . expand("<cword>") . "/j **" <Bar> cw<CR>
nnoremap <silent> <F8> :TlistToggle<CR>


if has('cscope')
   set cscopetag cscopeverbose
   if has('quickfix')
      set cscopequickfix=s-,c-,d-,i-,t-,e-
   endif
endif

if has('persistent_undo')
    set undofile
    set undodir=$HOME/.vim/undo
endif

