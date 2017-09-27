cat tweets.csv | csvprintf '%6$s\n' | grep -vE ^RT | sed -E 's,@[^ ]+ ,,g' > tweets.txt
