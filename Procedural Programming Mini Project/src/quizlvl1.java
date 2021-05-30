import java.util.Scanner;

public class quizlvl1{
	public static void main(String args[]){
		full();
	}
	
	public static void full() {
		question1();
		question2();
		question3();
		question4();
		question5();
		System.out.println("You got 234 points");
	}
	public static void question1() {
		System.out.println("Who is owner of Tesla?\n");
		System.out.println("1. Tim Cook");
		System.out.println("2. Bill Gates");
		System.out.println("3. Elon Musk");
		System.out.println("Please write out their full name: ");
		input();
	}
	public static void question2() {
		System.out.println("Who is owner of Amazon?");
		System.out.println("1. Jeff Bezos");
		System.out.println("2. Mohammed Afjal");
		System.out.println("3. Elon Musk");
		System.out.println("Please write out their full name: ");
		input();
	}
	public static void question3() {
		System.out.println("Who is owner of Facebook?");
		System.out.println("1. Will Smith");
		System.out.println("2. Mark Zuckerberg");
		System.out.println("3. Mohammed Hamza Ahad");
		System.out.println("Please write out their full name: ");
		input();
	}
	public static void question4() {
		System.out.println("Who is owner of Microsoft?");
		System.out.println("1. Bill Gates");
		System.out.println("2. Easa Akhter");
		System.out.println("3. Steve Jobs");
		System.out.println("Please write out their full name: ");
		input();
	}
	public static void question5() {
		String answer;
		System.out.println("Who is owner of Samsung?");
		System.out.println("1. Lee Kun-Hee");
		System.out.println("2. Eun Ke");
		System.out.println("3. Gi No-ka");
		System.out.println("Please write out their full name: ");
		input();
	}
	public static void input() {
		Scanner scanner = new Scanner(System.in);

		scanner.nextLine();
	}
}