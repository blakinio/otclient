param(
  [string]$OutputPath = (Join-Path $PSScriptRoot 'fixtures/synthetic-login-smoke.png')
)
Add-Type -AssemblyName System.Drawing
$bmp = New-Object System.Drawing.Bitmap 1024,640
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::None
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::SingleBitPerPixelGridFit
$bg = [System.Drawing.Color]::FromArgb(16,25,38)
$panel = [System.Drawing.Color]::FromArgb(31,45,61)
$line = [System.Drawing.Color]::FromArgb(198,160,78)
$text = [System.Drawing.Color]::FromArgb(235,235,235)
$muted = [System.Drawing.Color]::FromArgb(165,175,185)
$g.Clear($bg)
$panelBrush = New-Object System.Drawing.SolidBrush $panel
$linePen = New-Object System.Drawing.Pen $line,3
$textBrush = New-Object System.Drawing.SolidBrush $text
$mutedBrush = New-Object System.Drawing.SolidBrush $muted
$titleFont = [System.Drawing.Font]::new('Arial',[single]28,[System.Drawing.FontStyle]::Bold,[System.Drawing.GraphicsUnit]::Pixel)
$headerFont = [System.Drawing.Font]::new('Arial',[single]24,[System.Drawing.FontStyle]::Bold,[System.Drawing.GraphicsUnit]::Pixel)
$labelFont = [System.Drawing.Font]::new('Arial',[single]18,[System.Drawing.FontStyle]::Regular,[System.Drawing.GraphicsUnit]::Pixel)
$footerFont = [System.Drawing.Font]::new('Arial',[single]16,[System.Drawing.FontStyle]::Bold,[System.Drawing.GraphicsUnit]::Pixel)
$g.FillRectangle($panelBrush,180,70,664,500)
$g.DrawRectangle($linePen,180,70,664,500)
$g.DrawString('TIBIA VISION SAFE FIXTURE',$titleFont,$textBrush,258,100)
$g.DrawString('ACCOUNT LOGIN',$headerFont,$textBrush,390,175)
$g.DrawString('EMAIL',$labelFont,$mutedBrush,300,255)
$g.DrawRectangle($linePen,300,290,424,54)
$g.DrawString('PASSWORD',$labelFont,$mutedBrush,300,375)
$g.DrawRectangle($linePen,300,410,424,54)
$g.DrawString('NO SECRET DATA',$footerFont,$textBrush,407,510)
$dir = Split-Path -Parent $OutputPath
New-Item -ItemType Directory -Force $dir | Out-Null
$bmp.Save($OutputPath,[System.Drawing.Imaging.ImageFormat]::Png)
$footerFont.Dispose(); $labelFont.Dispose(); $headerFont.Dispose(); $titleFont.Dispose()
$mutedBrush.Dispose(); $textBrush.Dispose(); $linePen.Dispose(); $panelBrush.Dispose(); $g.Dispose(); $bmp.Dispose()
Write-Output $OutputPath

