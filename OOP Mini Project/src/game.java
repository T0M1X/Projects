import java.util.Scanner;
import java.util.concurrent.TimeUnit;
import java.util.Random;

public class game{
	public static void main(String[] args) {
		start();
	}
	
	public static void start() {
		String name;
		String choice = "p";
		
		System.out.println("Please enter the name of you new character.");
		name = input();
		
		while (!(choice.equals("a")) && !(choice.equals("b")) && !(choice.equals("c")) && !(choice.equals("d"))) {
			System.out.println("\nPlease enter the letter for your chosen character type.");
			System.out.println("CHOICES:");
			System.out.println("[A] - Magician");
			System.out.println("[B] - Archer");
			System.out.println("[C] - Swordsman");
			System.out.println("[D] - Ninja");
			choice = (input()).toLowerCase();
		}
		game_start(name,choice);
	}
	
	public static void game_start(String name, String character) {
		String stringType;
		int type;
		player[] person = {
				new magician(name), 
				new archer(name), 
				new swordsman(name), 
				new ninja(name)
				};
		if (character.equals("a")) {
			stringType = "Magician";
			type = 0;
		} else if (character.equals("b")) {
			stringType = "Archer";
			type = 1;
		} else if (character.equals("c")) {
			stringType = "Swordsman";
			type = 2;
		} else {
			stringType = "Ninja";
			type = 3;
		}
		System.out.println("\n\n");
		message(name+"!",70);
		message("It is time for you to embark on your quest as a "+ stringType+".",20);
		message("Find and defeat Gorg to win the game!",20);
		message("Traverse through the catacombs of Gorg's dungeon to find him!",20);
		message("At each room you will be given a choice to move to a different room.",20);
		message("In unexplored rooms you will find either treasure, an enemy or an empty room.",20);
		message("Be careful of Gorg's minions along the way.",20);
		int[][] map = {{0,0,1,0},{0,3,0,0},{1,0,0,0},{1,0,0,3},{2},{3,0,1,0},{1,0,0,0},{0,0,3,1},{1,0,0,0},{2},{3,1,1,1},{0,3,3,0},{0,0,0,0},{0,0,0,0},{2}};
		int posx = 0;
		int posy = 0;
		int potions = 0;
		String dir;
		boolean a = true;
		//Game loop
		while(a) {
			dir = decision(posx,posy);
			if ((dir.equals("left") && (posy%5 == 0 | posy%5 == 1))| (dir.equals("right") && (posy%5 == 2 | posy%5 == 3))) {
				posx = posx + 1;
			} else if (dir.equals("left") | dir.equals("right")) {
				posx = posx - 1;
			}
			if (dir.equals("up")) {
				posy = posy + 1;
			}
			if (dir.equals("down")) {
				posy = posy - 1;
			}
			if (dir.equals("inv")) {
				message("You have "+potions+" health potions left.",20);
				message("Your weapon is currently level " + person[type].getLevel() + ".",20);
				continue;
			}
			if (dir.equals("check")) {
				message(person[type].show_health(),20);
				continue;
			}
			if (dir.equals("restore")) {
				if (potions > 0) {
					message("Your health is restored to the max!",20);
					person[type].restore_health();
					message(person[type].show_health(),20);
					potions = potions - 1;
				} else {
					message("You have no more potions!",20);
				}
				continue;
			}
			
			message("You enter the next room....",20);
			if (map[posy][posx] == 0) {
				message("The room is empty",20);
				message("The emptiness of the room is daunting.",30);
			} else if (map[posy][posx] == 1) {
				message("One of gorg's minions lurks inside the room!",25);
				message("You feel like you should be afraid but you dont feel anything.",30);
				person[type] = fight_minion(person[type]);
				map[posy][posx] = 0;
				message("You have defeated one of Gorg's minion!",20);
			} else if (map[posy][posx] == 2) {
				if (posx == 0 && posy == 14) {
					message("This room is larger than the rest",70);
					message("You feel that the end is near",70);
					message("You don't want to fight but you wish to escape the dungeon.",70);
					message("Gorg looks down at you from his throne.",100);
					person[type] = fight_boss(person[type],false);
					message("CONGRATULATIONS",50);
					message("You defeated Gorg and made it to the end of the dungeon!",40);
					message("You look around and see no exit",40);
					message("You were always trapped",40);
					message("You are now trapped and lonely",40);
					message("You fade away and no one remembers you.",50);
					System.exit(0);
				} else {
					message("The room is filled with darkness",50);
					message("You wish to turn back",50);
					message("A soldier of Gorg inhabits the room",70);
					message("His presence pushes you away",70);
					message("You must fight him.",70);
					person[type] = fight_boss(person[type],true);
					if (posy == 9) {
						if (type == 0) {
							message(((magician)person[type]).getWarlock(),60);
						} else if (type == 1) {
							message(((archer)person[type]).getHunter(),60);
						} else if (type == 2) {
							message(((swordsman)person[type]).getBeserker(),60);
						} else {
							message(((ninja)person[type]).getShinobi(),60);
						}
					}
					
				}
			} else if (map[posy][posx] == 3) {
				int hp;
				hp = randInt(1,20);
				message("This room is bright and calming",30);
				if (hp > 5) {
					message("You found a health potion!",20);
					potions = potions + 1;
				} else {
					message("You found an upgrade!",20);
					person[type].increaseLevel();
				}
				message("You must move on.",30);
				map[posy][posx] = 0;
			}
		}
	}
	
	public static player fight_minion(player p) {
		int type = randInt(0,3);
		minion[] enemies = {
				new minion("Goblin",50, new String[][] {{"Bite","14"},{"Kick","7"}}),
				new minion("Troll",70, new String[][] {{"Stomp","9"},{"Swing club","18"}}),
				new minion("Orc",60, new String[][] {{"Bite","14"},{"Punch","8"}})
				};
		message("A "+ enemies[type].get_name() + " stands before you!",20);
		boolean cont = true;
		int choice;
		int damage;
		int attack;
		int randLoss;
		int randRestore;
		message(enemies[type].show_health(),20);
		while (cont == true){
			choice = 10;
			while (!(choice == 1) && !(choice == 2) && !(choice == 3) && !(choice == 4)){
				p.displayMoves();
				message(p.show_health(),20);
				message("Please select your move",20);
				choice = inputInt();
				if (choice == 4 && p.getDamage(3).equals("")) {
					choice = 10;
					System.out.println("You do not have a 4th move yet!");
				}
			}
			choice = choice - 1;
			message("You use "+p.getMoves()[choice][0],20);
			damage = Integer.parseInt(p.getDamage(choice))+p.getLevel()*randInt(1,4);
			if (damage > 20) {
				randLoss = randInt(1,12);
				if (randLoss > 9) {
					p.increaseMax(-1);
					message("Your max health went down after using a high damage attack!",20);
				}
			} else if (damage < 10) {
				randRestore = 8+randInt(0,4);
				p.increase_health(randRestore);
				message("You were able to restore "+randRestore+" health during your light attack!",20);
			}
			message("Your attack did "+damage+" damage!",20);
			enemies[type].lose_health(damage);
			message(enemies[type].show_health(),20);
			if (enemies[type].get_health() <= 0) {
				message("You defeated the "+enemies[type].get_name()+"!",20);
				message("Your max health has increased by 4!",20);
				p.increaseMax(4);
				if (enemies[type].get_name() == "Troll") {
					message("Your weapon was upgraded!",20);
					p.increaseLevel();
				}
				return p;
			}
			attack = randInt(0,2);
			message("The "+enemies[type].get_name()+" used "+ enemies[type].getMoves()[attack][0]+"!",20);
			damage = Integer.parseInt(enemies[type].getMoves()[attack][1]) + randInt(1,4);
			message("The "+enemies[type].get_name()+" did "+ damage+ " damage!",20);
			p.lose_health(damage);
			p.show_health();
			if (p.get_health() <= 0) {
				message("Unfortunatly you were defeated.",50);
				message("Maybe next time you can escape Gorg's dungeon!",40);
				System.exit(0);
			}
		}
		return p;
	}
	
	public static player fight_boss(player p, boolean mini) {
		int type = randInt(0,2);
		if (mini == false) {
			type = 2;
		}
		boss[] enemies = {
				new boss("Narcagua", 110, new String[][] {{"Bite","21"},{"Tail whip","17"},{"Scratch","13"}}),
				new boss("Rathian",100, new String[][] {{"Stomp","14"},{"Fireball","32"},{"Tail slam","15"}}),
				new boss("Gorg",160, new String[][] {{"Slash","35"},{"Punch","23"},{"Barge","14"}})
				};
		message(enemies[type].get_name() + " stands before you!",20);
		boolean cont = true;
		int choice;
		int damage;
		int attack;
		int randLoss;
		int randRestore;
		message(enemies[type].show_health(),20);
		while (cont == true){
			choice = 10;
			while (!(choice == 1) && !(choice == 2) && !(choice == 3) && !(choice == 4)){
				p.displayMoves();
				message(p.show_health(),30);
				message("Please select your move",20);
				choice = inputInt();
				if (choice == 4 && p.getDamage(3).equals("")) {
					choice = 10;
					System.out.println("You do not have a 4th move yet!");
				}
			}
			choice = choice - 1;
			message("You use "+p.getMoves()[choice][0],30);
			damage = Integer.parseInt(p.getDamage(choice))+p.getLevel()*randInt(1,4);
			if (Integer.parseInt(p.getDamage(choice)) > 20) {
				randLoss = randInt(1,12);
				if (randLoss > 9) {
					p.increaseMax(-1);
					message("Your max health went down after using a high damage attack!",20);
				}
			} else if (Integer.parseInt(p.getDamage(choice)) < 10) {
				randRestore = 8+randInt(0,4);
				p.increase_health(randRestore);
				message("You were able to restore "+randRestore+" health during your light attack!",20);
			}
			message("Your attack did "+damage+" damage!",30);
			enemies[type].lose_health(damage);
			message(enemies[type].show_health(),20);
			if (enemies[type].get_health() <= 0) {
				message("You defeated the "+enemies[type].get_name()+"!",30);
				message("Your max health has increased by 7!",30);
				p.increaseMax(7);
				message("Your weapon was upgraded!",20);
				p.increaseLevel();
				return p;
			}
			attack = randInt(0,2);
			message("The "+enemies[type].get_name()+" used "+ enemies[type].getMoves()[attack][0]+"!",30);
			damage = Integer.parseInt(enemies[type].getMoves()[attack][1]) + randInt(1,4);
			message("The "+enemies[type].get_name()+" did "+ damage+ " damage!",30);
			p.lose_health(damage);
			p.show_health();
			if (p.get_health() <= 0) {
				message("Unfortunatly you were defeated.",50);
				message("Maybe next time you can escape Gorg's dungeon!",40);
				System.exit(0);
			}
		}
		return p;
	}
	
	public static int randInt(int min, int max) {
		Random rand = new Random();
		return rand.nextInt(max-min)+min;
	}
	
	public static String decision(int x,int y) {
		String direction = "";
		int left = 0;
		int right = 0;
		int up = 0;
		int down = 0;
		
		if (x == 0) {
			up = 1;
		}
		if (x == 3 && (y%5 == 0 | y%5 == 2)) {
			up = 1;
		}
		if (x == 0 && y > 0) {
			down = 1;
		}
		if (x == 3 && (y%5 == 1 | y%5 == 3)) {
			down = 1;
		}
		if(!(y == 4 | y == 9)) {
			if (!(x == 3 && y%5 == 0) && !(x == 3 && y%5 == 1) && !(x == 0 && y%5 == 2) && !(x == 0 && y%5 == 3)) {
				left = 1;
			}
		}
		if(!(y == 4 | y == 9)) {
			if (!(x == 0 && y%5 == 0) && !(x == 0 && y%5 == 1) && !(x == 3 && y%5 == 2) && !(x == 3 && y%5 == 3)) {
				right = 1;
			}
		}
		
		String options = "";
		if (up == 1) {
			options = options + ", UP";
		}
		if (down == 1) {
			options = options + ", DOWN";
		}
		if (left == 1) {
			options = options + ", LEFT";
		}
		if (right == 1) {
			options = options + ", RIGHT";
		}
		
		String commands = "INV, RESTORE, CHECK";
		
		while (!(direction.equals("left")) && !(direction.equals("right")) && !(direction.equals("up")) && !(direction.equals("down")) && !(direction.equals("inv")) && !(direction.equals("check")) && !(direction.equals("restore"))) {
			System.out.println("\n");
			System.out.println("Your can go: " + options.substring(1,options.length())+"\n");
			System.out.println("Type INV to look at your inventory");
			System.out.println("Type RESTORE to use a health potion");
			System.out.println("Type CHECK to check your health");
			message("Please type the direction you wish to go.",20);
			direction = input().toLowerCase();
			System.out.println("\n");
			if (options.toLowerCase().contains(direction) && direction.length() > 1) {
				message("You go " + direction.toUpperCase(),20);
			} else if (commands.toLowerCase().contains(direction) && direction.length() > 2) {
				direction.toUpperCase();
			} else {
				message("You cannot do " + direction.toUpperCase() + "!",20);
				direction = "";
			}
		}
		return direction;
	}
	
	//This function allows the user to input a string a then it will return that string.
	public static String input() {
		Scanner scanner = new Scanner(System.in);
		String textInput;

		textInput = scanner.nextLine();
		return textInput;
	}
	
	public static void message(String text, int time){
		for (char c : text.toCharArray()) {
		    System.out.print(c);
		    sleep(time);
		}
		System.out.println("\n");
	}
	
	public static void sleep(int time){
		try {
			TimeUnit.MILLISECONDS.sleep(time);
		} catch (InterruptedException e) {
			return;
		}
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

class inv{
	int potion;
	int upgrade;
	int uber;
}

class magician extends player{
	String warlock;

	public magician(String name){
		super(name, new String[][] {{"Fireball","23"},{"Wack","13"},{"Punch","4"},{"",""}});
		warlock = "You have developed from a magician to a Warlock! If you return home you will become a GrandMaster Magician!";
	}
	
	public String show_health() {
		return("Magician. Your health is "+super.get_health()+"/"+super.get_max());
	}
	
	public void addMove() {
		super.setMove("Light strike","28");
	}
	
	public String getWarlock() {
		return warlock;
	}
	
	public void setWarlock(String s) {
		warlock = s;
	}
}

class archer extends player{
	String hunter;
	
	public archer(String name){
		super(name , new String[][] {{"Shoot","16"},{"Stab","10"},{"Kick","5"},{"",""}});
		hunter = "You have have leveled up from standard archer to Hunter! Your eyes are piercing, you will become legendary if you return home!";
	}
	
	public String show_health() {
		return("Archer. Your health is "+super.get_health()+"/"+super.get_max());
	}
	
	public void addMove() {
		super.setMove("Triple shot","35");
	}
	
	public String getHunter() {
		return hunter;
	}
	
	public void setHunter(String s) {
		hunter = s;
	}
}

class swordsman extends player{
	String beserker;
	
	public swordsman(String name){
		super(name, new String[][] {{"Slash","28"},{"Wack","13"},{"Barge","2"},{"",""}});
		beserker = "You have now leveled up from swordsman to Legendary Beserket! If you make it out your people will be known as a Legend!";
	}
	
	public String show_health() {
		return("Swordsman. Your health is "+super.get_health()+"/"+super.get_max());
	}
	
	public void addMove() {
		super.setMove("Quick slash","7");
	}
	
	public String getBeserker() {
		return beserker;
	}
	
	public void setBeserker(String s) {
		beserker = s;
	}
}

class ninja extends player{
	String shinobi;
	
	public ninja(String name){
		super(name, new String[][]{{"Shurikan","17"},{"Kunai","19"},{"Shadow punch","8"},{"",""}});
		shinobi = "You have now become a fully fledged Shinobi! Fight to the end to return to your home and make your village proud!";
	}
	
	public String show_health() {
		return("Ninja. Your health is "+super.get_health()+"/"+super.get_max());
	}
	
	public void addMove() {
		super.setMove("Sneak Strike", "28");
	}
	
	public String getShinobi() {
		return shinobi;
	}
	
	public void setShinobi(String s) {
		shinobi = s;
	}
}

abstract class player{
	private String name;
	private int max_health;
	private int health;
	private int weapon;
	private String moves[][] = new String[4][2];
	
	public player(String name, String[][] moves){
		this.name = name;
		health = 100;
		max_health = 100;
		weapon = 100;
		weapon = 1;
		this.moves = moves;
	}
	
	public void lose_health(int damage){
		health = health - damage;
	}
	
	public void restore_health() {
		health = max_health;
	}
	
	public void increaseMax(int num) {
		max_health = max_health + num;
	}
	
	public void restore_weapon() {
		weapon = max_health;
	}
	
	public String show_health() {
		return("Your health is "+health+"/"+max_health);
	}
	
	public int get_max() {
		return max_health;
	}
	
	public int get_health() {
		return health;
	}
	
	public String[][] getMoves(){
		return moves;
	}
	
	public int getLevel() {
		return weapon;
	}
	
	public void increaseLevel() {
		weapon=weapon+1;
		if (weapon == 4) {
			addMove();
			try {
				TimeUnit.SECONDS.sleep(1);
			} catch (InterruptedException e) {
				return;
			}
			System.out.println("You have a new move!");
			try {
				TimeUnit.SECONDS.sleep(1);
			} catch (InterruptedException e) {
				return;
			}
			System.out.println("Your new move is called " + moves[3][0] + " and it has damage of " + moves[3][1]);
			try {
				TimeUnit.SECONDS.sleep(1);
			} catch (InterruptedException e) {
				return;
			}
		}
	}
	
	public void displayMoves() {
		System.out.println("Your moves:");
		for (int i = 0; i < 4; i++) {
			if (moves[i][0] == "") {
				continue;
			}
			System.out.println("["+(i+1)+"] - " + moves[i][0] + " --- Base Damage - "+ moves[i][1]);
		}
	}
	
	public String getDamage(int a) {
		return moves[a][1];
	}
	
	public String get_name() {
		return name;
	}
	
	public void increase_health(int num) {
		health = health + num;
	}
	
	public void setMove(String move, String damage) {
		moves[3][0] = move;
		moves[3][1] = damage;
	}
	
	public void addMove() {
		setMove("","");
	}
}

class minion{
	private String name;
	private int max_health;
	private int health;
	private String moves[][] = new String[2][2];
	
	public minion(String name, int max, String moves[][]) {
		this.name = name;
		max_health = max;
		health = max;
		this.moves = moves;
	}
	
	public void lose_health(int damage){
		health = health - damage;
	}
	
	public String show_health() {
		return("The health of the "+ name +" is "+health+"/"+max_health);
	}
	
	public int get_health() {
		return health;
	}
	
	public String[][] getMoves(){
		return moves;
	}
	
	public String get_name() {
		return name;
	}
	
}

class boss{
	private String name;
	private int max_health;
	private int health;
	private String moves[][] = new String[3][2];
	
	public boss(String name, int max, String moves[][]) {
		this.name = name;
		max_health = max;
		health = max;
		this.moves = moves;
	}
	
	public void lose_health(int damage){
		health = health - damage;
	}
	
	public String show_health() {
		return("The health of the "+ name +" is "+health+"/"+max_health);
	}
	
	public int get_health() {
		return health;
	}
	
	public String[][] getMoves(){
		return moves;
	}
	
	public String get_name() {
		return name;
	}
}