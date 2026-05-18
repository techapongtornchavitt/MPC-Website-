$path = 'C:\Users\Chavit\Downloads\brand guidlines mpc\portfolio.html'
$html = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)

function Item($file, $alt, $load) {
  $svg = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg>'
  return "      <div class=""gallery-item"" data-img=""$file"" data-alt=""$alt"">`r`n        <img src=""$file"" alt=""$alt"" loading=""$load"" decoding=""async"">`r`n        <div class=""pg-overlay""><span class=""pg-expand-icon"">$svg</span></div>`r`n      </div>"
}

$anchor1 = '      <div class="gallery-item" data-img="Portfolio experience.jpg"'
$insert1 = (Item 'portfolio.jpg'   'Industrial chain delivery - red curtain truck loaded with crated shipment'   'lazy') + "`r`n" +
           (Item 'portfolio 1.jpg' 'TRIO forged chain link - close-up quality inspection on-site'                'lazy') + "`r`n" +
           (Item 'portfolio 3.jpg' 'Chain system delivery - bulk crate shipment by truck to client site'         'lazy') + "`r`n" +
           (Item 'portfolio 4.jpg' 'MPC warehouse - forklift loading bulk chain crates for dispatch'             'lazy') + "`r`n"

$html = $html.Replace($anchor1, $insert1 + $anchor1)

$anchor2 = '    </div><!-- /gallery-grid -->'
$insert2 = (Item 'portfolio 2.jpg' 'DBC Roller Chain 80-2 - bulk shipment with product specification catalog' 'lazy') + "`r`n" +
           (Item 'portfolio 5.jpg' 'Industrial chain installation - hoisting heavy chain assembly on-site'     'lazy') + "`r`n" +
           (Item 'portfolio 6.jpg' 'MPC engineers - on-site technical inspection and measurement'              'lazy') + "`r`n`r`n"

$html = $html.Replace($anchor2, $insert2 + $anchor2)

$html = $html.Replace('>1 / 18<', '>1 / 25<')

[System.IO.File]::WriteAllText($path, $html, [System.Text.UTF8Encoding]::new($false))
Write-Host 'Done - 7 images added, counter updated to 1 / 25'
