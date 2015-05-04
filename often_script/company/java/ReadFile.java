import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.io.FileReader;
import java.io.BufferedReader;
public class ReadFile{
 
   public static void main(String args[]){
     File file = new File("tmall_product.txt");
     //FileInputStream input_stream = new FileInputStream(file);
     FileReader fr = new FileReader("/home/peng/company/java/tmall_product.txt");
     BufferedReader bufr = new BufferedReader(fr);
     String content = bufr.readLine();
     System.out.println(content);
 
    }
}
