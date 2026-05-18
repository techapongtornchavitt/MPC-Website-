$path = 'C:\Users\Chavit\Downloads\brand guidlines mpc\portfolio.html'
$html = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)

function Item($file, $alt) {
  $svg = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg>'
  return "      <div class=""gallery-item"" data-img=""$file"" data-alt=""$alt"">`r`n        <img src=""$file"" alt=""$alt"" loading=""lazy"" decoding=""async"">`r`n        <div class=""pg-overlay""><span class=""pg-expand-icon"">$svg</span></div>`r`n      </div>"
}

# Insert portfolio 7 + 8 after portfolio 4.jpg block (mid-gallery, before experience section)
$anchor1 = '      <div class="gallery-item" data-img="Portfolio experience.jpg"'
$insert1 = (Item 'portfolio 7.jpg' 'Sugar mill chain links - bulk crate inspection before shipment') + "`r`n" +
           (Item 'portfolio 8.jpg' 'Technician assembling sugar cane elevator chain with star attachments') + "`r`n"
$html = $html.Replace($anchor1, $insert1 + $anchor1)

# Append portfolio 9 + 10 at end of gallery grid
$anchor2 = '    </div><!-- /gallery-grid -->'
$insert2 = (Item 'portfolio 9.jpg'  'MPC Chain Specialist organising roller chain order at supplier warehouse') + "`r`n" +
           (Item 'portfolio 10.jpg' 'MPC team unloading industrial chain shipment from shipping container') + "`r`n`r`n"
$html = $html.Replace($anchor2, $insert2 + $anchor2)

# Update counter 25 -> 29
$html = $html.Replace('>1 / 25<', '>1 / 29<')

[System.IO.File]::WriteAllText($path, $html, [System.Text.UTF8Encoding]::new($false))
Write-Host 'Done - 4 images added, counter updated to 1 / 29'
