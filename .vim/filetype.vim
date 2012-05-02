if exists("did_load_filetypes")
  finish
endif
augroup filetypedetect
  " au! commands to set the filetype go here
  au! BufNewFile,BufRead *.cl setf opencl
  au! BufNewFile,BufRead *.rsh set filetype=c
augroup END
augroup filetypedetect
  au! BufNewFile,BufRead *.vert,*.frag,*.fp,*.vp,*.glsl setf glsl
augroup END
