# set arg separator strings
Param([String]$Separator = " - ")

Add-Type -AssemblyName System.Globalization
Add-Type -AssemblyName System.Drawing

# get en-US Culture ID
$enCultureId = [System.Globalization.CultureInfo]::GetCultureInfo("en-US").LCID

# enumerate font ja and en name
(New-Object System.Drawing.Text.InstalledFontCollection).Families |
    ForEach-Object {
        if (!($_.Name.Length -eq 0)){
            ("{0}{1}{2}" -f $_.Name, $Separator, $_.GetName($enCultureId))
        }
    }
