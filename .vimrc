syn on
set hidden
set history=2000
set expandtab
set shellslash
colorscheme tir_black
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
filetype plugin indent on

let g:ctrlp_mruf_relative = 1
let g:ctrlp_custom_ignore = {
   \ 'dir':  '\.git$\|\.hg$\|\.svn$\',
   \ 'file': '\.o$\|\.pyc$\|\.swp$\|\.exe$\|\.so$\|\.dll$\|\.DS_Store$',
   \ 'link': 'SOME_BAD_SYMBOLIC_LINKS',
   \ }

" Re-map leader modifier to ','
let mapleader = ","

" Show whitespace
set listchars=tab:>-,trail:·,eol:$
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
nnoremap <silent> <F8> :TlistToggle<CR>
