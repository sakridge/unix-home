mkdir -p bundle

clone_or_update () {
    if [ -d "$2" ]; then
        echo "Pulling.. $2"
        pushd $2 && git pull
        popd
    else
        echo "Cloning.. $2"
        git clone $1 $2
    fi
}
clone_or_update https://github.com/tpope/vim-pathogen.git bundle/vim-pathogen
clone_or_update https://github.com/kien/ctrlp.vim.git bundle/ctrlp.vim
clone_or_update https://github.com/rust-lang/rust.vim.git bundle/rust.vim
clone_or_update https://github.com/ldx/vim-indentfinder.git bundle/vim-indentfinder
