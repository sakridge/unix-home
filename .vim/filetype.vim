if exists("did_load_filetypes")
  finish
endif
augroup filetypedetect
  " au! commands to set the filetype go here
  au! BufNewFile,BufRead *.cl setf opencl
augroup END
