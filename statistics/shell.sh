cat ETH.txt \
 | grep Strategy \
 | sed 's/[^-.0-9]*//g'  \
 | sed '/--/d' \
 | sed '/^[[:space:]]*$/d' \
 > ETH.csv