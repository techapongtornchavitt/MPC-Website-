# Fix "Our Specialized Industries" cover images in index.html
# Problem: images were assigned to wrong industry cards, and one card
# was using a catalog/data page image instead of a proper cover photo.
#
# Correct assignments:
#   Cement  card  -> "cement specialized industry.png"
#   Palm Oil card -> "Palm oil specialized industry.png"
#   Sugar   card  -> "Sugar specialized industry.png"

$path = 'C:\Users\Chavit\Downloads\brand guidlines mpc\index.html'
$html = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)

# Step 1: Cement card — was using a data/catalog page image
$html = $html.Replace(
  'src="Cement industry info page .png" alt="Cement Industry"',
  'src="cement specialized industry.png" alt="Cement Industry"'
)

# Step 2: Palm Oil card — was using the Sugar image
$html = $html.Replace(
  'src="Sugar specialized industry.png" alt="Palm Oil Industry"',
  'src="Palm oil specialized industry.png" alt="Palm Oil Industry"'
)

# Step 3: Sugar card — was using the Cement image
$html = $html.Replace(
  'src="cement specialized industry.png" alt="Sugar Industry"',
  'src="Sugar specialized industry.png" alt="Sugar Industry"'
)

[System.IO.File]::WriteAllText($path, $html, [System.Text.UTF8Encoding]::new($false))
Write-Host 'index.html industry cover images fixed.'

# Verify
$check = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
$lines = $check -split "`n" | Select-String 'industry-card-img' -Context 0,1
foreach ($l in $lines) {
  Write-Host $l.Context.PostContext[0].Trim()
}
