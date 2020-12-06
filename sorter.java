
import java.io.FileWriter;   // Import the FileWriter class
import java.util.Random;
import java.text.DecimalFormat;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.stream.Stream;
import java.io.*; 
import java.util.ArrayList;
import java.util.Scanner;
import java.util.Arrays;

public class sorter {

    
    public static void main(String[] args) {
        File sorted_folder = new File("sortedAll");
    

        ArrayList<String> f = new ArrayList<String>();
        try {
            File myObj = new File("sort/invalids.txt");
            Scanner myReader = new Scanner(myObj);
            while (myReader.hasNextLine()) {
                String data = myReader.nextLine();
                f.add(data);
            }
        myReader.close();
        } catch (FileNotFoundException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
        int num;
        for (String data : f) {
            if (data.indexOf('s') == 0) {
                num = 45;
                String[] pp = createPP(num, "small", data);
                make(data, "small", pp, num);
            } else if (data.indexOf('m') == 0) {
                num = 190;
                String[] pp = createPP(num, "medium", data);
                make(data, "medium", pp, num);
            } else {
                num = 1225;
                String[] pp = createPP(num, "large", data);
                make(data, "large", pp, num);
            }
        }



    }
    public static String[] createPP(int num, String size, String data) {
        File myObj = new File("phase2/inputs/" + size + "/" + data);
        double[][] pp = new double[num][4];

        try {
            Scanner myReader = new Scanner(myObj);
            int counter = -2;
            
            while (counter < (4 * num) && myReader.hasNext()) {
                String dataa = myReader.next();
                if (counter >= 0) {
                    pp[counter / 4][counter % 4] = Double.parseDouble(dataa);
                }
                counter += 1;
            }
            myReader.close();
        }
        catch (FileNotFoundException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }


        for (int i = 0; i < num; i += 1) {
            if (pp[i][0] > pp[i][1]) {
                double temp = pp[i][0];
                pp[i][0] = pp[i][1];
                pp[i][1] = temp;
            }
        }
        Arrays.sort(pp, (a, b) -> Double.compare(a[0] * 64.0 + a[1], b[0] * 64.0 + b[1]));
        return convert(pp);
    }

    //writes to for all in the string array.
    public static void write(String[] lines, String name) {
        try {
            FileWriter myWriter = new FileWriter(name);
            for (int i = 0; i < lines.length; i += 1) {
                myWriter.write(lines[i] + "\n");
            }
            myWriter.close();
            System.out.println("Successfully wrote to the file.");
        }
        catch (IOException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
    }


    //creates test.txt if it doesn't exist.
    public static void make(String name, String size, String[] pp, int num) {
        String name2 = name;
        name = "sortedAll/" + name;
        try
            {
            File myFile = new File(name);
            if (myFile.createNewFile()) {
                System.out.println("File created: " + myFile.getName());
            } else {
                System.out.println("File already exists.");
            }
        }
        catch (IOException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }

        addInputs(name2, size, pp, num);
    }
    //name2 = .in file name
    //name = .sortall file location
    public static void addInputs(String name2, String size, String[] pp, int num) {
        try {
            String name = "sortedAll/" + name2;
            File myObj = new File("phase2/inputs/" + size + "/" + name2);
            Scanner myReader = new Scanner(myObj);
            int counter = 0;
            String[] temp = new String[2 + num];
            while (counter < 2) {
                String data = myReader.nextLine();
                temp[counter] = data;
                counter += 1;
            }
            for (int i = 0; i < num; i += 1) {
                temp[i + 2] = pp[i];
            }

            
            myReader.close();
            write(temp, name);
        }
        catch (FileNotFoundException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
    }

    public static String[] convert(double[][] pp) {
        String[] r = new String[pp.length];
        for (int i = 0; i < pp.length; i += 1) {
            String add = "";
            for (int j = 0; j < 3; j += 1) {
                if (j < 2) {
                    int temp = (int)pp[i][j];
                    add += temp;
                } else {
                    add += pp[i][j];
                }
                add += " ";
            }
            add += pp[i][3];
            r[i] = add;
        }
        return r;
    }
  

}
