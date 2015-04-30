#!/bin/bash
a=10
b=10
c=9
d=11
e="yupengbo"
f="yupengbo"
g="wangruijing"
if test $a -eq $b;then
    echo "111111111111111"
else
    echo "222222222222222"
fi

if test $a -gt $c;then
    echo "333333333333333"
fi

if test $e;then
    echo "444444444444444"
fi

if test $f=$e;then
    echo "555555555555555"
fi

if [ $a -eq $b ];then
    echo "666666666666666"
fi

if test $f!=$g;then
   echo "521"
fi

if test $a -eq 12;then
   echo "equal 12"
elif test $a -eq 10;then
   echo "equal 10"
fi
