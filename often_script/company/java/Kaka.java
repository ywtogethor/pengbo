class Cluo{
  int a = 10;
  int b = 20;
  public void method(){
     System.out.println("====================");
     System.out.println(a+b);
     System.out.println(this.a);
     System.out.println(a);
     System.out.println("====================");
   }

}


public class Kaka{
   static  int a = 10;
   int b = 20;
   public static void main(String args[]){
        Kaka kk = new Kaka();
        System.out.println(a);
        System.out.println(kk.b);
        Cluo c = new Cluo();
        c.method();
   }
}
