$path = 'C:\Users\Chavit\Downloads\brand guidlines mpc\styles.css'
$css = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)

$append = @"


/* -- Translation flash prevention ------------------------------------------------
   Hide body until lang.js has applied the correct language, then
   reveal it instantly. The 600 ms safety timer in lang.js ensures
   the page always becomes visible even on very slow connections.
   ------------------------------------------------------------------------------- */
html:not(.lang-ready) body {
  opacity: 0;
  pointer-events: none;
  user-select: none;
}
body {
  transition: opacity 0.1s ease;
}
"@

[System.IO.File]::WriteAllText($path, $css + $append, [System.Text.UTF8Encoding]::new($false))
Write-Host "Done"
