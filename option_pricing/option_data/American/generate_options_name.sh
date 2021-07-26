#!/bin/bash

out=""

for o in `cat hosts.ini`
do
  o = "ssh root@&o -c 'hostname'"
  out+=$o
done

echo $out