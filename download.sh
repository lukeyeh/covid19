date=$(date +'%B-%-d-%Y')

start="https://www.mass.gov/doc/covid-19-cases-in-massachusetts-as-of-"
end="-accessible/download"
date_lower=$(echo "$date" | tr '[:upper:]' '[:lower:]')

download_str="${start}${date_lower}${end}"
date_save=$(date '+%Y-%m-%d')

wget -O "${date_save}.docx" $download_str
