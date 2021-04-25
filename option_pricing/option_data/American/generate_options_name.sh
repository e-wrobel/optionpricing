#!/bin/bash

out=""

for o in `ls | grep NFLX | cut -d '.' -f1`
  do out+=", $o"
done

echo $out