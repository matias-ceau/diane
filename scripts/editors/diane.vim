" diane, vim integration
"
" Install: cp diane.vim ~/.vim/plugin/diane.vim
" Or with vim-plug:
"   Plug '/path/to/diane/scripts/editors/diane.vim'

if exists('g:loaded_diane')
  finish
endif
let g:loaded_diane = 1

" Configuration
if !exists('g:diane_default_tags')
  let g:diane_default_tags = []
endif

if !exists('g:diane_encrypt')
  let g:diane_encrypt = 0
endif

" Capture current buffer to diane
function! DianeCaptureBuffer()
  let l:content = join(getline(1, '$'), "\n")
  let l:cmd = 'diane, -v'

  " Add tags if configured
  if !empty(g:diane_default_tags)
    let l:cmd .= ' --tags ' . join(g:diane_default_tags, ',')
  endif

  " Add encryption if configured
  if g:diane_encrypt
    let l:cmd .= ' --encrypt'
  endif

  " Execute
  let l:result = system(l:cmd, l:content)
  echo l:result
endfunction

" Capture visual selection to diane
function! DianeCaptureSelection() range
  let l:content = join(getline(a:firstline, a:lastline), "\n")
  let l:cmd = 'diane, -v'

  " Add tags if configured
  if !empty(g:diane_default_tags)
    let l:cmd .= ' --tags ' . join(g:diane_default_tags, ',')
  endif

  " Add encryption if configured
  if g:diane_encrypt
    let l:cmd .= ' --encrypt'
  endif

  " Execute
  let l:result = system(l:cmd, l:content)
  echo l:result
endfunction

" Capture with tags prompt
function! DianeCaptureWithTags()
  let l:tags = input('Tags (comma-separated): ')
  let l:content = join(getline(1, '$'), "\n")
  let l:cmd = 'diane, -v'

  if !empty(l:tags)
    let l:cmd .= ' --tags ' . l:tags
  endif

  let l:result = system(l:cmd, l:content)
  echo l:result
endfunction

" Quick capture from command line
function! DianeQuickCapture(...)
  let l:text = join(a:000, ' ')
  if empty(l:text)
    let l:text = input('Quick capture: ')
  endif

  if !empty(l:text)
    let l:result = system('diane, -v', l:text)
    echo l:result
  endif
endfunction

" Search diane records and open in buffer
function! DianeSearch(query)
  let l:results = system('diane, --search "' . a:query . '"')

  " Open in new split
  split __DianeSearch__
  setlocal buftype=nofile
  setlocal bufhidden=wipe
  setlocal noswapfile

  " Insert results
  call setline(1, split(l:results, "\n"))
endfunction

" Commands
command! DianeCapture call DianeCaptureBuffer()
command! DianeCaptureSelection '<,'>call DianeCaptureSelection()
command! DianeCaptureWithTags call DianeCaptureWithTags()
command! -nargs=* DianeQuick call DianeQuickCapture(<f-args>)
command! -nargs=1 DianeSearch call DianeSearch(<f-args>)

" Key mappings (customize as needed)
" <leader>dc - Capture buffer
nnoremap <leader>dc :DianeCapture<CR>
" <leader>ds - Capture selection
vnoremap <leader>ds :DianeCaptureSelection<CR>
" <leader>dt - Capture with tags
nnoremap <leader>dt :DianeCaptureWithTags<CR>
" <leader>dq - Quick capture
nnoremap <leader>dq :DianeQuick
" <leader>df - Search
nnoremap <leader>df :DianeSearch

" Statusline integration (optional)
function! DianeStatus()
  let l:count = system('diane, --list 2>/dev/null | grep -c "^─"')
  return 'diane: ' . trim(l:count) . ' records'
endfunction

" Add to statusline with:
" set statusline+=%{DianeStatus()}
