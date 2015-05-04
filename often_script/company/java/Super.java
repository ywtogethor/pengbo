class Parent{
   String name = "cluo";
   public Parent(String data){
      System.out.println(data);
   }
   public void kaka(){
      System.out.println("kaka");
      System.out.println(getClass().getName());
   }

}
class SubParent extends Parent{
   public SubParent(String data){
      super("I am cluo");
      super.kaka();
      System.out.println(data);
     
    }  

}

public class Super{
  public static void main(String args[]){
      System.out.println("123");
      SubParent kk = new SubParent("I am cluo too");
      kk.kaka();
   }
}
