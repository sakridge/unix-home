while true
do
   pmap -p $1 > pmap.bad.maybe-fixed.$(date '+%Yy%mm%dd%Hh%Mm%Ss%Nns')
done
