import java.math.BigInteger;

class aaa{
   static int a = 10;
   final int b =20;
  
}


public class Cluo{    
  public static void main(String args[]){
       aaa m = new aaa();
       aaa.a = 20;
       m.b = 30;
       System.out.println(m.a);
       System.out.println(m.b);
     
   }
}
