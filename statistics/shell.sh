cat ADA.txt \
 | grep Strategy \
 | sed 's/[^-.0-9]*//g'  \
 | sed '/--/d' \
 | sed '/^[[:space:]]*$/d' \
 > ADA.csv

cat BNB.txt \
 | grep Strategy \
 | sed 's/[^-.0-9]*//g'  \
 | sed '/--/d' \
 | sed '/^[[:space:]]*$/d' \
 > BNB.csv

cat DASH.txt \
 | grep Strategy \
 | sed 's/[^-.0-9]*//g'  \
 | sed '/--/d' \
 | sed '/^[[:space:]]*$/d' \
 > DASH.csv

cat ETH.txt \
 | grep Strategy \
 | sed 's/[^-.0-9]*//g'  \
 | sed '/--/d' \
 | sed '/^[[:space:]]*$/d' \
 > ETH.csv

cat LTC.txt \
 | grep Strategy \
 | sed 's/[^-.0-9]*//g'  \
 | sed '/--/d' \
 | sed '/^[[:space:]]*$/d' \
 > LTC.csv

cat XRP.txt \
 | grep Strategy \
 | sed 's/[^-.0-9]*//g'  \
 | sed '/--/d' \
 | sed '/^[[:space:]]*$/d' \
 > XRP.csv

cat BAT.txt \
 | grep Strategy \
 | sed 's/[^-.0-9]*//g'  \
 | sed '/--/d' \
 | sed '/^[[:space:]]*$/d' \
 > BAT.csv

cat BTC.txt \
 | grep Strategy \
 | sed 's/[^-.0-9]*//g'  \
 | sed '/--/d' \
 | sed '/^[[:space:]]*$/d' \
 > BTC.csv

cat EOS.txt \
 | grep Strategy \
 | sed 's/[^-.0-9]*//g'  \
 | sed '/--/d' \
 | sed '/^[[:space:]]*$/d' \
 > EOS.csv

cat LINK.txt \
 | grep Strategy \
 | sed 's/[^-.0-9]*//g'  \
 | sed '/--/d' \
 | sed '/^[[:space:]]*$/d' \
 > LINK.csv

cat XMR.txt \
 | grep Strategy \
 | sed 's/[^-.0-9]*//g'  \
 | sed '/--/d' \
 | sed '/^[[:space:]]*$/d' \
 > XMR.csv