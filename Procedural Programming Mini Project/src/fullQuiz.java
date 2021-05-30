//by Atif Abdur-Rahman

import java.util.Scanner;
import java.util.LinkedList;
import java.util.Queue;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;

public class fullQuiz{
	public static void main(String args[]){
		full();
	}
	
// This method runs all the question methods and also adds up and outputs the final score to the user.
	public static void full() {
		question score = new question();
		score.setFinalScore(0);
		int finalScore;
		int numQs;
		String name;
		String[] sortedArray;
		Queue<Integer> questionQueue = new LinkedList<>();
		finalScore = score.getFinalScore();
		System.out.println("Please enter your name: ");
		name = input();
		System.out.println("Try to get the least amount of points by getting correct answers");
		System.out.println("The less known an answer is the less points you will get");
		System.out.println("How many questions would you like to answer? Please enter a number between 1 and 5");
		numQs = inputInt();
		while (numQs < 1 | numQs > 5) {
			System.out.println("How many questions would you like to answer? Please enter a number between 1 and 5");
			numQs = inputInt();
		}
		questionQueue = makeQueue(numQs);
		for (int i = 0; i < numQs; i++) {
			finalScore = finalScore + pickQuestion(questionQueue.remove());
		}
		score.setFinalScore(finalScore);
		System.out.println("You got " + score.getFinalScore() + " points in total out of " + (numQs*100) + ".");
		createScoreFile();
		saveScore(name,(finalScore/numQs));
		sortedArray = bubbleSort(readScores());
		displayScores(sortedArray);
		}
	
// This method contains the bubble sort algorithm and will be used to sort the highscores in the file.
	public static String[] bubbleSort(String[] a) {
	    boolean sorted = false;
	    int temp;
	    String tempS;
	    String[] names = new String[(a.length)/2];
	    int[] scores = new int[(a.length)/2];
	    for (int i = 0; i < ((a.length)/2); i++) {
	    	names[i] = a[2*i];
	    	scores[i] = Integer.parseInt(a[2*i + 1]);
	    }
	    while(sorted == false) {
	        sorted = true;
	        for (int i = 0; i < scores.length - 1; i++) {
	            if (scores[i] > scores[i+1]) {
	                temp = scores[i];
	                scores[i] = scores[i+1];
	                scores[i+1] = temp;
	                tempS = names[i];
	                names[i] = names[i+1];
	                names[i+1] = tempS;
	                sorted = false;
	            }
	        }
	    }
	    for (int i=0; i < scores.length; i++) {
	    	a[2*i] = names[i];
	    	a[2*i + 1] = Integer.toString(scores[i]);
	    }
	    return a;
	}
	
//This method displays the top 5 scores and the name of the player that got the score
	public static void displayScores(String[] sortedScores) {
		int maxScores = 0;
		maxScores = readFileLines();
		if (maxScores > 5) {
			maxScores = 5;
		}
		System.out.println("The highest " + maxScores + " scores are:");
		for (int i=0; i < maxScores; i++) {
			System.out.println("Number " + (i+1) +" is a score of " + sortedScores[2*i + 1] + " by " + sortedScores[2*i]);
		}
	}
	
//This method will create a new file that will be used to store the scoreboard
	public static void createScoreFile() {
		try {
			File file = new File("Scoreboard.txt");
			if (file.createNewFile()) {
				System.out.println("Score Board file created.");
			} else {
				System.out.println("Score Board file already exists.");
			}
		} catch (IOException e) {
			System.out.println("A file error occured");
		}
	}
	
//This method will save a new result inside the file
	public static void saveScore(String name, int score) {
		String [] temp = readScores();
		try {
			File file = new File("Scoreboard.txt");
			FileOutputStream fos = new FileOutputStream(file);
			BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(fos));
			for (int i = 0; i < (temp.length); i = i + 2) {
				writer.write(temp[i] + "," + temp[i+1]);
				writer.newLine();
			}
			writer.write(name + "," + score);
			writer.newLine();
			writer.close();
			System.out.println("Your score has been added to the scoreboard.");
		} catch (IOException e) {
			System.out.println("A file error occured");
		}
	}
	
//This method is used to read the scores that are currently in the file
	public static String[] readScores() {
		int numLines;
		numLines = readFileLines();
		String[] temp = new String[(numLines*2)];
		String[] row = new String[2];
		try {
			File file = new File("Scoreboard.txt");
			Scanner scanner = new Scanner(file);
			for (int i=0; i < numLines; i++) {
				row = scanner.nextLine().split(",");
				temp[2*i] = row[0];
				temp[2*i+1] = row[1];
			}
			scanner.close();
		} catch (FileNotFoundException e) {
			System.out.println("A file error occured");
		}
		return temp;
	}
	
//This method is used to count how many lines of data are there in the file.
	public static int readFileLines() {
		int lines = 0;
		try {
			BufferedReader reader = new BufferedReader(new FileReader("Scoreboard.txt"));
			while (reader.readLine() != null) {
				lines = lines + 1;
			};
			reader.close();
		} catch (IOException e){
			System.out.println("A file error occured");
		}
		return lines;
	}

//This method will run a question method using the order of the queue that in passed into the program.
	public static int pickQuestion(int q){
		int r = 0;
		if (q == 1) {
			r = question1();
		} else if (q == 2) {
			r = question2();
		} else if (q == 3) {
			r = question3();
		} else if (q == 4) {
			r = question4();
		} else if (q == 5) {
			r = question5();
		}
		return r;
	}
	
//This method is used to create a queue, the queue will hold a random order numbers which correlate to the order in which the questions will be asked
	public static Queue<Integer> makeQueue(int num) {
		int rand = 0;
		int[] usedNumbers = new int[num];
		Boolean in = true;
		Queue<Integer> queue = new LinkedList<>();
		
		for (int i=0; i < num; i++) {
			while (in == true) {
				rand = ((int)(Math.random()*num)) + 1;
				for (int j=0; j < num; j++) {
					if (rand == usedNumbers[j]) {
						in = true;
						break;
					}
					in = false;
				}
			}
			in = true;
			queue.add(rand);
			usedNumbers[i] = rand;
		}
		
		return queue;
	}
		
//This method creates question 1 record and runs the askQuestion method.
	public static int question1() { 
		int score;
		String[] ops = {"CSGO","Fortnite","Valorant"};
		int[] pos = {12,88,100};
		question q1 = createQuestion("Name a top 5 most popular twitch games in 2019", ops,pos);
		score = askQuestion(q1);
		
		return score;
	}
//This method creates question 2 record and runs the askQuestion method.
	public static int question2() { 
		int score;
		String[] ops = {"Luxemburg","USA","Qatar"};
		int[] pos = {34,100,56};
		question q2 = createQuestion("Name a top 5 country with the highest GDP per capita", ops,pos);
		score = askQuestion(q2);
		
		return score;
	}
//This method creates question 3 record and runs the askQuestion method.
	public static int question3() { 
		int score;
		String[] ops = {"Will Smith","Steve Chen","Chad Hurley"};
		int[] pos = {100,35,23};
		question q3 = createQuestion("Name a founder of youtube", ops,pos);
		score = askQuestion(q3);
		
		return score;
	}
//This method creates question 4 record and runs the askQuestion method.
	public static int question4() { 
		int score;
		String[] ops = {"Larry Page","Sergey Brin","Mark Zuckerberg"};
		int[] pos = {45,23,100};
		question q4 = createQuestion("Name a founder of google", ops,pos);
		score = askQuestion(q4);
		
		return score;
	}
//This method creates question 5 record and runs the askQuestion method.
	public static int question5() { 
		int score;
		String[] ops = {"Steve Jobs","Steve Wozniak","Tim Apple"};
		int[] pos = {89,11,100};
		question q5 = createQuestion("Name a founder of apple", ops,pos);
		score = askQuestion(q5);
		
		return score;
	}

//This function allows the user to input a string a then it will return that string.
	public static String input() {
		Scanner scanner = new Scanner(System.in);
		String textInput;

		textInput = scanner.nextLine();
		return textInput;
	}
	
//This method asks the question to the user and then also returns the points that the user will get for that answer.
	public static int askQuestion(question a) {
		String answer;
		int score;
		System.out.println(a.question);
		System.out.println("1. " + a.options[0]);
		System.out.println("2. " + a.options[1]);
		System.out.println("3. " + a.options[2]);
		System.out.println("Please write out their full name: ");
		answer = input();
		if ((answer.toLowerCase()).equals(a.options[0].toLowerCase())) {
			score = a.points[0];
		} else if ((answer.toLowerCase()).equals(a.options[1].toLowerCase())) {
			score = a.points[1];
		} else if ((answer.toLowerCase()).equals(a.options[2].toLowerCase())){
			score = a.points[2];
		} else {
			score = 100;
			System.out.println("That was incorrect!");
		}
		System.out.println("You have gained " + score + " points\n");
		return score;
	}
	
//This method creates a new question record and fills out the arrays.
	public static question createQuestion(String myQuestion, String[] options, int[] points) {
		question a = new question();
		
		a.question = myQuestion;
		for (int i = 0; i < 3; i++) {
			a.options[i] = options[i];
			a.points[i] = points[i];
		}
		
		return a;
	}
	
//This function allows the user to input an integer and it contains validation so that they cannot enter another data type.
	public static int inputInt() {
		Scanner scanner = new Scanner(System.in);
		int intInput;
		boolean isInt;
		intInput = 0;
		isInt = false;
		do {
			while (!scanner.hasNextInt()) {
				System.out.println("Please enter a number");
				scanner.nextLine();
			}
			intInput = scanner.nextInt();
			isInt = true;
			break;
		} while (isInt == false);
		return intInput;
	}
}

//This is the creation of the question class that uses two arrays for the question and the score
class question{
	String question;
	String[] options = new String[3];
	int[] points = new int[3];
	
	private int finalScore = 0;
	
	public int getFinalScore() {
		return finalScore;
	}
	
	public void setFinalScore(int newFinalScore) {
		this.finalScore = newFinalScore;
	}
}