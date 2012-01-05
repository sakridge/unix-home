syn on
set expandtab
set shellslash
colorscheme wombat
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

" tell VIM to always put a status line in, even if there is only one window
set laststatus=2

" Set the status line
set stl=%f\ %m\ Line:%l/%L[%p%%]\ Col:%v\ Buf:#%n\ [%b][0x%B]
