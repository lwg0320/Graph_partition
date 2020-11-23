import java.io.File;  // Import the File class
import java.io.IOException;  // Import the IOException class to handle errors
import java.io.FileWriter;   // Import the FileWriter class
import java.util.Random;
import java.text.DecimalFormat;

public class eccentric {
    public static void main(String[] args) {
        Random rand = new Random();
        make();
        String[] lines = new String[1227];
        lines[0] = "50";
        lines[1] = "1000";
        
        int offset = 2;
        int count = 0;
        for (int i = 0; i < 49; i += 1) {
            for (int j = i + 1; j < 50; j += 1) {
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
        write(lines);
    }

    //creates test.txt if it doesn't exist.
    public static void make() {
        try
            {
            File myFile = new File("test50.txt");
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
    public static void write(String[] lines) {
        try {
            FileWriter myWriter = new FileWriter("test50.txt");
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

//java eccentric.java