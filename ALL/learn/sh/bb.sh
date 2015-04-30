#!/bin/bash
a=10
while test $a -lt 20;do
  echo $a
#  a=`expr $a + 1`
  let a=$a+1
done
