import java.io.File;  // Import the File class
import java.io.IOException;  // Import the IOException class to handle errors
import java.io.FileWriter;   // Import the FileWriter class
import java.util.Random;
import java.text.DecimalFormat;

public class eccentric {
    public static void main(String[] args) {
        Random rand = new Random();
        String name = "test50.txt";
        make(name);
        String[] lines = new String[1227];
        int num = 50;
        lines[0] = String.valueOf(num);
        lines[1] = "1000";
        int offset = 2;
        int count = 0;
        for (int i = 0; i < num - 1; i += 1) {
            for (int j = i + 1; j < num; j += 1) {
                double randomHappy = rand.nextDouble() * 100;
                double randomStress = rand.nextDouble() * 100;
                DecimalFormat df = new DecimalFormat("##.###");
                String temp = "" + i + " " + j + " " +
                    "" + df.format(randomHappy) + " " +
                    df.format(randomStress);
                lines[offset] = temp;
                offset += 1;
            }
        }
        write(lines, name);


        name = "test20.txt";
        make(name);
        String[] lines2 = new String[192];
        num = 20;
        lines[0] = String.valueOf(num);
        lines[1] = "250";
        offset = 2;
        for (int i = 0; i < num - 1; i += 1) {
            for (int j = i + 1; j < num; j += 1) {
                double randomHappy = rand.nextDouble() * 100;
                double randomStress = rand.nextDouble() * 100;
                DecimalFormat df = new DecimalFormat("##.###");
                String temp = "" + i + " " + j + " " +
                    "" + df.format(randomHappy) + " " +
                    df.format(randomStress);
                lines2[offset] = temp;
                offset += 1;
            }
        }
        write(lines2, name);



        name = "test10.txt";
        make(name);
        String[] lines3 = new String[47];
        num = 10;
        lines[0] = String.valueOf(num);
        lines[1] = "80";
        offset = 2;
        for (int i = 0; i < num - 1; i += 1) {
            for (int j = i + 1; j < num; j += 1) {
                double randomHappy = rand.nextDouble() * 100;
                double randomStress = rand.nextDouble() * 100;
                DecimalFormat df = new DecimalFormat("##.###");
                String temp = "" + i + " " + j + " " +
                    "" + df.format(randomHappy) + " " +
                    df.format(randomStress);
                lines3[offset] = temp;
                offset += 1;
            }
        }
        write(lines3, name);
    }

    //creates test.txt if it doesn't exist.
    public static void make(String name) {
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
    }

    //writes to test.txt for all in the string array.
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
}
