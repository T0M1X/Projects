import java.util.Scanner;

public class quizlvl2{
	public static void main(String args[]){
		full();
	}
	
	public static void full() {
		question1();
		question2();
		question3();
		question4();
		question5();
		System.out.println("You got 5 points");
	}
	public static void question1() {
		String answer;
		System.out.println("Who is owner of Tesla?\n");
		System.out.println("1. Tim Cook");
		System.out.println("2. Bill Gates");
		System.out.println("3. Elon Musk");
		System.out.println("Please write out their full name: ");
		answer = input();
	}
	public static void question2() {
		String answer;
		System.out.println("Who is owner of Amazon?");
		System.out.println("1. Jeff Bezos");
		System.out.println("2. Mohammed Afjal");
		System.out.println("3. Elon Musk");
		System.out.println("Please write out their full name: ");
		answer = input();
	}
	public static void question3() {
		String answer;
		System.out.println("Who is owner of Facebook?");
		System.out.println("1. Will Smith");
		System.out.println("2. Mark Zuckerberg");
		System.out.println("3. Mohammed Hamza Ahad");
		System.out.println("Please write out their full name: ");
		answer = input();
	}
	public static void question4() {
		String answer;
		System.out.println("Who is owner of Microsoft?");
		System.out.println("1. Bill Gates");
		System.out.println("2. Easa Akhter");
		System.out.println("3. Steve Jobs");
		System.out.println("Please write out their full name: ");
		answer = input();
	}
	public static void question5() {
		String answer;
		System.out.println("Who is owner of Samsung?");
		System.out.println("1. Lee Kun-Hee");
		System.out.println("2. Eun Ke");
		System.out.println("3. Gi No-ka");
		System.out.println("Please write out their full name: ");
		answer = input();
	}
	public static String input() {
		Scanner scanner = new Scanner(System.in);
		String textInput;

		textInput = scanner.nextLine();
		return textInput;
	}
}