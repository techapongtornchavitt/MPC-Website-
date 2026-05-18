# Fix catalog data images — swap to correctly-named files
# cement-industry-catalog.png   → showed Sugar content    (WRONG)
# sugar-industry-catalog.png    → showed Palm Oil content (WRONG)
# palm-oil-industry-catalog.png → showed Maintenance      (WRONG)
# Correct files already exist: "Cement/Sugar/Palm oil industry info page .png"

$dir = 'C:\Users\Chavit\Downloads\brand guidlines mpc'

# ── cement-industry.html ──────────────────────────────────────────────────────
$f = Join-Path $dir 'cement-industry.html'
$h = [System.IO.File]::ReadAllText($f, [System.Text.Encoding]::UTF8)
$h = $h.Replace('src="cement-industry-catalog.png"', 'src="Cement industry info page .png"')
[System.IO.File]::WriteAllText($f, $h, [System.Text.UTF8Encoding]::new($false))
Write-Host 'cement-industry.html updated'

# ── sugar-industry.html ───────────────────────────────────────────────────────
$f = Join-Path $dir 'sugar-industry.html'
$h = [System.IO.File]::ReadAllText($f, [System.Text.Encoding]::UTF8)
$h = $h.Replace('src="sugar-industry-catalog.png"', 'src="Sugar industry info page .png"')
[System.IO.File]::WriteAllText($f, $h, [System.Text.UTF8Encoding]::new($false))
Write-Host 'sugar-industry.html updated'

# ── palm-oil-industry.html ────────────────────────────────────────────────────
$f = Join-Path $dir 'palm-oil-industry.html'
$h = [System.IO.File]::ReadAllText($f, [System.Text.Encoding]::UTF8)
$h = $h.Replace('src="palm-oil-industry-catalog.png"', 'src="Palm oil industry info page .png"')
[System.IO.File]::WriteAllText($f, $h, [System.Text.UTF8Encoding]::new($false))
Write-Host 'palm-oil-industry.html updated'

Write-Host 'All 3 industry catalog images fixed.'
