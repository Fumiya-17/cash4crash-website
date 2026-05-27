$brands = @('audi', 'bmw', 'ford', 'mercedes', 'volkswagen', 'toyota', 'honda', 'hyundai', 'nissan', 'porsche')
foreach ($b in $brands) {
    $res = Invoke-RestMethod -Uri "https://unsplash.com/napi/search/photos?query=$b`+car&per_page=3"
    Write-Output "--- $b ---"
    $res.results | ForEach-Object { $_.urls.raw }
}
