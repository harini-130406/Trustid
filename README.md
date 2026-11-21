1)Write a Java program to read marks in three subjects, calculate the average, and display the grade according to the following criteria: A (90 and above), B (75–89), C (50–74), and F (below 50). Create a Maven project and configure an Azure Pipeline to compile the application and generate the JAR file. 


MarksGradeCalculator — Complete Practical Procedure
Step 1: Create the Maven Project in IntelliJ
Open IntelliJ IDEA.
Click File → New → Project.
Select Java.
Project Name: MarksGradeCalculator
Build System: Maven
JDK: 17
If only JDK 21 is installed, use 21 temporarily and switch to 17 when available.
Click Create.
Step 2: Create Main.java
Navigate to:
src → main → java → org.example
Create a Java class named:
Main.java
Paste the following code:

package org.example;

import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter marks in Subject 1: ");
        int mark1 = sc.nextInt();

        System.out.print("Enter marks in Subject 2: ");
        int mark2 = sc.nextInt();

        System.out.print("Enter marks in Subject 3: ");
        int mark3 = sc.nextInt();

        double average = (mark1 + mark2 + mark3) / 3.0;

        System.out.println("Average Marks: " + average);

        if (average >= 90) {
            System.out.println("Grade: A");
        }
        else if (average >= 75) {
            System.out.println("Grade: B");
        }
        else if (average >= 50) {
            System.out.println("Grade: C");
        }
        else {
            System.out.println("Grade: F");
        }

        sc.close();
    }
}
Step 3: Create/Configure pom.xml
In the project root, open pom.xml and replace the contents with:

<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>MarksGradeCalculator</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <build>
        <plugins>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.13.0</version>
                <configuration>
                    <source>17</source>
                    <target>17</target>
                </configuration>
            </plugin>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <version>3.4.2</version>
                <configuration>
                    <archive>
                        <manifest>
                            <mainClass>org.example.Main</mainClass>
                        </manifest>
                    </archive>
                </configuration>
            </plugin>

        </plugins>
    </build>

</project>
Step 4: Run the Java Program
Open Main.java.
Click the green Run ▶ button beside main().
Enter the three marks.
Example:
Enter marks in Subject 1: 95
Enter marks in Subject 2: 90
Enter marks in Subject 3: 85
Average Marks: 90.0
Grade: A
Step 5: Build the JAR Using Maven
Open the IntelliJ Terminal in the project root.
Execute:
mvn clean package
Verify the generated JAR in:
target/MarksGradeCalculator-1.0-SNAPSHOT.jar
Run the JAR:
java -jar target/MarksGradeCalculator-1.0-SNAPSHOT.jar
Step 6: Create a GitHub Repository
Go to https://github.com/.
Sign in.
Click + → New repository.
Repository name:
MarksGradeCalculator

Select Public or Private.
Do not initialize with README.
Click Create repository.
Step 7: Push the Project to GitHub
Open IntelliJ Terminal in the project root (MarksGradeCalculator).
Execute the following commands one by one:
git init

git add .

git commit -m "Initial commit - Marks Grade Calculator"
Connect the GitHub repository:
git remote add origin https://github.com/YOUR_USERNAME/MarksGradeCalculator.git
Replace YOUR_USERNAME with your GitHub username.
git branch -M main

git push -u origin main
Verify that your project files are visible on GitHub.
Step 8: Create azure-pipelines.yml
In IntelliJ:
Right-click the project root MarksGradeCalculator.
Click New → File.
Create a file named:
azure-pipelines.yml

Ensure it is at the same level as pom.xml.
Paste the following code:

trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'

steps:
  - task: JavaToolInstaller@0
    inputs:
      versionSpec: '17'
      jdkArchitectureOption: 'x64'
      jdkSourceOption: 'PreInstalled'

  - task: Maven@4
    inputs:
      mavenPomFile: 'pom.xml'
      goals: 'clean package'
      options: ''
      publishJUnitResults: true
      testResultsFiles: '**/surefire-reports/TEST-*.xml'
      javaHomeOption: 'JDKVersion'
      jdkVersionOption: '1.17'
      jdkArchitectureOption: 'x64'

  - task: PublishBuildArtifacts@1
    inputs:
      PathtoPublish: 'target'
      ArtifactName: 'Java-JAR'
      publishLocation: 'Container'
Step 9: Push azure-pipelines.yml to GitHub
Open IntelliJ Terminal.
git add .

git commit -m "Add Azure pipeline configuration"

git push
Verify that azure-pipelines.yml is visible in your GitHub repository.
Step 10: Create Azure DevOps Pipeline
Go to https://dev.azure.com/.
Sign in.
Create an organization if required.
Click New Project.
Project name:
MarksGradeCalculator

Click Create.
Open Pipelines → Pipelines.
Click New Pipeline.
Select GitHub.
Authorize Azure DevOps to access GitHub.
Select your repository:
MarksGradeCalculator

Select Existing Azure Pipelines YAML file.
Select branch:
main
14. Select YAML file:
/azure-pipelines.yml

Click Continue.
Click Run.
Step 11: Verify the Pipeline
Wait until the pipeline finishes.
Verify that the following steps are successful:
GitHub repository checkout
Java 17 configuration
Maven clean package
Compilation
JAR generation
Artifact publishing
Step 12: Download the JAR Artifact
Open the successful pipeline run.
Go to Summary.
Locate Artifacts.
Click Java-JAR.
Download the artifact.
Verify that the JAR file exists.
Expected JAR:
MarksGradeCalculator-1.0-SNAPSHOT.jar
Step 13: Set JDK 17 in IntelliJ
If you are currently using JDK 21:
Go to File → Project Structure → Project.
Set Project SDK → JDK 17.
Set Language Level → 17.
Click Apply → OK.
Then:
Go to File → Settings.
Navigate to Build, Execution, Deployment → Build Tools → Maven → Runner.
Set JRE → JDK 17.
Click Apply → OK.
In pom.xml, ensure both are set to 17:
<maven.compiler.source>17</maven.compiler.source>
<maven.compiler.target>17</maven.compiler.target>
Final Project Structure
MarksGradeCalculator
│
├── .idea
├── .mvn
├── src
│   ├── main
│   │   ├── java
│   │   │   └── org.example
│   │   │       └── Main.java
│   │   └── resources
│   ├── test
│   ├── .gitignore
├── pom.xml
└── azure-pipelines.yml
Final execution order:
IntelliJ → Java Program → Maven pom.xml → Run → mvn clean package → GitHub Repository → Push → azure-pipelines.yml → Push → Azure Pipeline → Build → JAR Artifact

2       Develop a Java application to calculate an electricity bill based on the units consumed, using the following rates: ₹1.50 per unit for the first 100 units, ₹2.50 per unit for the next 100 units, and ₹4.00 per unit for units exceeding 200. Build the application as a Maven project and configure an Azure Pipeline to compile the source code and generate the JAR artifact.

package org.example;

import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter electricity units consumed: ");
        int units = sc.nextInt();

        double bill;

        if (units <= 100) {
            bill = units * 1.50;
        }
        else if (units <= 200) {
            bill = (100 * 1.50) + ((units - 100) * 2.50);
        }
        else {
            bill = (100 * 1.50) + (100 * 2.50) + ((units - 200) * 4.00);
        }

        System.out.println("Electricity Bill: Rs. " + bill);

        sc.close();
    }
}
1           Develop a Java application to calculate simple interest based on the principal amount, rate of interest, and time period provided as input. Build the application as a Maven project and configure an Azure Pipeline to compile the source code and generate the JAR artifact.

package org.example;

import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter Principal Amount: ");
        double principal = sc.nextDouble();

        System.out.print("Enter Rate of Interest: ");
        double rate = sc.nextDouble();

        System.out.print("Enter Time Period (in years): ");
        double time = sc.nextDouble();

        double simpleInterest = (principal * rate * time) / 100;

        System.out.println("Simple Interest: Rs. " + simpleInterest);

        sc.close();
    }
}



   Develop a Java calculator application to perform addition, subtraction, multiplication, and division, including division-by-zero handling. Write JUnit test cases for all arithmetic operations and configure an Azure Pipeline using Maven to build the application and run the regression tests.

Experiment 5 – Java Calculator using Maven, JUnit & Azure Pipeline
Step 1: Create a Maven Project in IntelliJ IDEA
Open IntelliJ IDEA.
Click New Project.
Select Maven.
Enter the following:
Name: CalculatorApp
JDK: 17
GroupId: org.example
ArtifactId: CalculatorApp
Click Create.
Step 2: Create the Project Structure
Create the following files and folders inside the Maven project.
Project structure
CalculatorApp
│
├── pom.xml
├── azure-pipelines.yml
│
└── src
    ├── main
    │   └── java
    │       └── org
    │           └── example
    │               ├── Calculator.java
    │               └── Main.java
    │
    └── test
        └── java
            └── org
                └── example
                    └── CalculatorTest.java
Step 3: Create Calculator.java
Location:
src/main/java/org/example/Calculator.java
package org.example;

public class Calculator {

    public int add(int a, int b) {
        return a + b;
    }

    public int subtract(int a, int b) {
        return a - b;
    }

    public int multiply(int a, int b) {
        return a * b;
    }

    public double divide(int a, int b) {
        if (b == 0) {
            throw new ArithmeticException("Division by zero");
        }
        return (double) a / b;
    }
}
Step 4: Create Main.java
Location:
src/main/java/org/example/Main.java
package org.example;

import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        Calculator calc = new Calculator();

        System.out.println("1. Addition");
        System.out.println("2. Subtraction");
        System.out.println("3. Multiplication");
        System.out.println("4. Division");

        System.out.print("Enter your choice: ");
        int choice = sc.nextInt();

        System.out.print("Enter first number: ");
        int a = sc.nextInt();

        System.out.print("Enter second number: ");
        int b = sc.nextInt();

        try {
            switch (choice) {
                case 1:
                    System.out.println("Result: " + calc.add(a, b));
                    break;

                case 2:
                    System.out.println("Result: " + calc.subtract(a, b));
                    break;

                case 3:
                    System.out.println("Result: " + calc.multiply(a, b));
                    break;

                case 4:
                    System.out.println("Result: " + calc.divide(a, b));
                    break;

                default:
                    System.out.println("Invalid choice");
            }
        } catch (ArithmeticException e) {
            System.out.println(e.getMessage());
        }

        sc.close();
    }
}
Step 5: Configure pom.xml
Open the root pom.xml file and replace its contents with:
Location: CalculatorApp/pom.xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>CalculatorApp</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.13.0</version>
            </plugin>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.2.5</version>
            </plugin>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <version>3.4.2</version>
                <configuration>
                    <archive>
                        <manifest>
                            <mainClass>org.example.Main</mainClass>
                        </manifest>
                    </archive>
                </configuration>
            </plugin>

        </plugins>
    </build>

</project>
After saving, click the Maven reload icon in IntelliJ to download the JUnit dependencies.
Step 6: Create JUnit Test Cases
Location:
src/test/java/org/example/CalculatorTest.java
package org.example;

import org.junit.Test;
import static org.junit.Assert.*;

public class CalculatorTest {

    Calculator calc = new Calculator();

    @Test
    public void testAddition() {
        assertEquals(10, calc.add(5, 5));
    }

    @Test
    public void testSubtraction() {
        assertEquals(5, calc.subtract(10, 5));
    }

    @Test
    public void testMultiplication() {
        assertEquals(25, calc.multiply(5, 5));
    }

    @Test
    public void testDivision() {
        assertEquals(5.0, calc.divide(25, 5), 0.001);
    }

    @Test(expected = ArithmeticException.class)
    public void testDivisionByZero() {
        calc.divide(10, 0);
    }
}
Test cases
Test
Input
Expected Output
Addition
5 + 5
10
Subtraction
10 − 5
5
Multiplication
5 × 5
25
Division
25 ÷ 5
5
Division by zero
10 ÷ 0
ArithmeticException

Step 7: Run JUnit Tests in IntelliJ
Open CalculatorTest.java.
Right-click anywhere inside the file.
Select Run CalculatorTest.
Observe the test results in the Run window.
Run tests | IntelliJ IDEA Documentation
Expected result: all 5 tests should pass.
Step 8: Run the Maven Build Locally
Open the Terminal in IntelliJ at the project root.
Run:
mvn clean test
This command:
Cleans the previous build.
Compiles the Java source code.
Compiles the JUnit test cases.
Runs all test cases.
Generates test reports.
Next, run:
mvn clean package
This builds the application and generates the JAR file.
Expected output:
BUILD SUCCESS
Generated JAR location:
target/CalculatorApp-1.0-SNAPSHOT.jar
Step 9: Create the Azure Pipeline YAML
Create a new file in the root folder of the project.
File name:
azure-pipelines.yml
Location:
CalculatorApp
├── pom.xml
├── azure-pipelines.yml
Paste the following:
trigger:
- main

pool:
  vmImage: ubuntu-latest

steps:

- task: JavaToolInstaller@0
  inputs:
    versionSpec: '17'
    jdkArchitectureOption: 'x64'
    jdkSourceOption: 'PreInstalled'
  displayName: 'Install Java 17'

- script: |
    java -version
    mvn -version
    mvn clean test
  displayName: 'Build and Run Regression Tests'

- script: mvn clean package
  displayName: 'Generate JAR Artifact'

- task: PublishBuildArtifacts@1
  inputs:
    PathtoPublish: 'target'
    ArtifactName: 'Calculator-JAR'
    publishLocation: 'Container'
  displayName: 'Publish JAR Artifact'
Step 10: Upload the Project to GitHub
Create a GitHub repository named:
CalculatorApp
Open the IntelliJ Terminal in the project root and execute:
git init
git add .
git commit -m "Calculator Maven project with JUnit tests"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/CalculatorApp.git
git push -u origin main
Replace YOUR_USERNAME with your GitHub username.
Step 11: Create the Azure Pipeline
Open Azure DevOps.
Sign in.
Select your organization.
Create or open a project.
Navigate to Pipelines → New Pipeline.
Select GitHub as the source.
Authorize Azure DevOps to access GitHub if prompted.
Select the CalculatorApp repository.
Choose Existing Azure Pipelines YAML file.
Select branch main.
Select /azure-pipelines.yml.
Click Run.
Step 12: Verify the Pipeline Execution
The Azure Pipeline should execute the following stages:
Install Java 17
Compile Java application
Run JUnit regression tests
Generate JAR file
Publish build artifact
Expected result:
BUILD SUCCESS
5 Tests
0 Failures
0 Errors
Step 13: Download the Generated JAR
Open your Azure Pipeline run.
Go to Summary.
Locate Artifacts.
Click Calculator-JAR.
Download the artifact.
Verify that the JAR file is present.
Expected JAR:
CalculatorApp-1.0-SNAPSHOT.jar
Step 14: Execute the JAR (Optional)
Run the JAR locally from the terminal:
java -jar target/CalculatorApp-1.0-SNAPSHOT.jar
Example output:
1. Addition
2. Subtraction
3. Multiplication
4. Division
Enter your choice: 1
Enter first number: 10
Enter second number: 20
Result: 30
1           Develop a Java application to determine whether a student has passed or failed based on the marks obtained (Pass: marks ≥ 50; Fail: marks < 50). Write JUnit test cases for marks 35, 50, 75, and 100, and configure an Azure Pipeline using Maven to build the application and run the regression tests.
Experiment 6 – Student Pass/Fail Application using Maven, JUnit & Azure Pipeline
Aim
To develop a Java application that determines whether a student has passed or failed based on marks (Pass: marks ≥ 50; Fail: marks < 50), write JUnit test cases for marks 35, 50, 75, and 100, and configure an Azure Pipeline using Maven to build the application and run regression tests.
Step 1: Create Maven Project in IntelliJ IDEA
Open IntelliJ IDEA.
Click New Project.
Select Maven.
Enter:
Name: StudentPassFail
JDK: 17
GroupId: org.example
ArtifactId: StudentPassFail
Click Create.
Step 2: Create Project Structure
Create the following files:
StudentPassFail
│
├── pom.xml
├── azure-pipelines.yml
│
└── src
    ├── main
    │   └── java
    │       └── org
    │           └── example
    │               ├── StudentResult.java
    │               └── Main.java
    │
    └── test
        └── java
            └── org
                └── example
                    └── StudentResultTest.java
Step 3: Create StudentResult.java
Location: src/main/java/org/example/StudentResult.java
package org.example;

public class StudentResult {

    public String checkResult(int marks) {
        if (marks >= 50) {
            return "Pass";
        } else {
            return "Fail";
        }
    }
}
Step 4: Create Main.java
Location: src/main/java/org/example/Main.java
package org.example;

import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter student marks: ");
        int marks = sc.nextInt();

        StudentResult result = new StudentResult();

        System.out.println("Result: " + result.checkResult(marks));

        sc.close();
    }
}
Step 5: Configure pom.xml
Open the root pom.xml and replace its contents with:
Location: StudentPassFail/pom.xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>StudentPassFail</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.13.0</version>
            </plugin>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.2.5</version>
            </plugin>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <version>3.4.2</version>
                <configuration>
                    <archive>
                        <manifest>
                            <mainClass>org.example.Main</mainClass>
                        </manifest>
                    </archive>
                </configuration>
            </plugin>

        </plugins>
    </build>

</project>
Save the file and reload Maven dependencies.
Step 6: Create JUnit Test Cases
Create StudentResultTest.java.
Location: src/test/java/org/example/StudentResultTest.java
package org.example;

import org.junit.Test;
import static org.junit.Assert.*;

public class StudentResultTest {

    StudentResult result = new StudentResult();

    @Test
    public void testFailWith35Marks() {
        assertEquals("Fail", result.checkResult(35));
    }

    @Test
    public void testPassWith50Marks() {
        assertEquals("Pass", result.checkResult(50));
    }

    @Test
    public void testPassWith75Marks() {
        assertEquals("Pass", result.checkResult(75));
    }

    @Test
    public void testPassWith100Marks() {
        assertEquals("Pass", result.checkResult(100));
    }
}
Test Cases
Test Case
Marks
Expected Result
Test 1
35
Fail
Test 2
50
Pass
Test 3
75
Pass
Test 4
100
Pass

Step 7: Run JUnit Tests in IntelliJ
Open StudentResultTest.java.
Right-click inside the file.
Click Run StudentResultTest.
Check the test results.
Expected result:
Tests passed: 4
Failures: 0
Errors: 0
Step 8: Run Maven Tests
Open IntelliJ Terminal and execute:
mvn clean test
Expected:
BUILD SUCCESS
To build the JAR:
mvn clean package
The JAR will be generated inside:
target/StudentPassFail-1.0-SNAPSHOT.jar
Step 9: Create Azure Pipeline YAML
Create a file named azure-pipelines.yml in the project root, beside pom.xml.
Location: StudentPassFail/azure-pipelines.yml
trigger:
- main

pool:
  vmImage: ubuntu-latest

steps:

- task: JavaToolInstaller@0
  inputs:
    versionSpec: '17'
    jdkArchitectureOption: 'x64'
    jdkSourceOption: 'PreInstalled'
  displayName: 'Install Java 17'

- script: |
    java -version
    mvn -version
    mvn clean test
  displayName: 'Build and Run Regression Tests'

- script: mvn clean package
  displayName: 'Generate JAR Artifact'

- task: PublishBuildArtifacts@1
  inputs:
    PathtoPublish: 'target'
    ArtifactName: 'StudentPassFail-JAR'
    publishLocation: 'Container'
  displayName: 'Publish JAR Artifact'
Step 10: Upload Project to GitHub
Create a GitHub repository named StudentPassFail.
Open the IntelliJ Terminal in your project folder:
git init
git add .
git commit -m "Student Pass Fail Maven project with JUnit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/StudentPassFail.git
git push -u origin main
Replace YOUR_USERNAME with your GitHub username.
Step 11: Create Azure Pipeline
Open Azure DevOps.
Sign in to your organization.
Open your project.
Go to Pipelines → New Pipeline.
Select GitHub.
Authorize Azure DevOps if prompted.
Select the StudentPassFail repository.
Choose Existing Azure Pipelines YAML file.
Select branch main.
Choose /azure-pipelines.yml.
Click Run.
Step 12: Verify Pipeline Execution
The pipeline executes the following steps:
Install Java 17.
Compile the Java application.
Run the JUnit regression tests.
Generate the JAR file.
Publish the artifact.
Expected result:
BUILD SUCCESS

Tests run: 4
Failures: 0
Errors: 0
Step 13: Download the JAR Artifact
Open the successful pipeline run.
Go to Summary.
Under Artifacts, click StudentPassFail-JAR.
Download the artifact.
Verify that the JAR file exists.
Expected file:
StudentPassFail-1.0-SNAPSHOT.jar
Step 14: Execute the Application (Optional)
java -jar target/StudentPassFail-1.0-SNAPSHOT.jar
Example output:
Enter student marks: 75
Result: Pass
1           Develop a Java application to determine whether a given year is a leap year. Write JUnit test cases covering leap years, non-leap years, and century years, and configure an Azure Pipeline using Maven to build the application and run the regression tests.
Experiment 7 – Leap Year Application using Maven, JUnit & Azure Pipeline
Step 1: Create a Maven Project in IntelliJ IDEA
Open IntelliJ IDEA.
Click New Project.
Select Maven.
Enter:
Name: LeapYearApp
JDK: 17
GroupId: org.example
ArtifactId: LeapYearApp
Click Create.
Step 2: Create Project Structure
Create the following files:
LeapYearApp
│
├── pom.xml
├── azure-pipelines.yml
│
└── src
    ├── main
    │   └── java
    │       └── org
    │           └── example
    │               ├── LeapYear.java
    │               └── Main.java
    │
    └── test
        └── java
            └── org
                └── example
                    └── LeapYearTest.java
Step 3: Create LeapYear.java
Location: src/main/java/org/example/LeapYear.java
package org.example;

public class LeapYear {

    public boolean isLeapYear(int year) {
        if (year % 400 == 0) {
            return true;
        } else if (year % 100 == 0) {
            return false;
        } else if (year % 4 == 0) {
            return true;
        } else {
            return false;
        }
    }
}
Step 4: Create Main.java
Location: src/main/java/org/example/Main.java
package org.example;

import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter a year: ");
        int year = sc.nextInt();

        LeapYear leapYear = new LeapYear();

        if (leapYear.isLeapYear(year)) {
            System.out.println(year + " is a Leap Year");
        } else {
            System.out.println(year + " is not a Leap Year");
        }

        sc.close();
    }
}
Step 5: Configure pom.xml
Location: LeapYearApp/pom.xml
Replace the contents with:
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>LeapYearApp</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.13.0</version>
            </plugin>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.2.5</version>
            </plugin>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <version>3.4.2</version>
                <configuration>
                    <archive>
                        <manifest>
                            <mainClass>org.example.Main</mainClass>
                        </manifest>
                    </archive>
                </configuration>
            </plugin>

        </plugins>
    </build>

</project>
Save the file and reload Maven dependencies.
Step 6: Create JUnit Test Cases
Location: src/test/java/org/example/LeapYearTest.java
package org.example;

import org.junit.Test;
import static org.junit.Assert.*;

public class LeapYearTest {

    LeapYear leapYear = new LeapYear();

    @Test
    public void testLeapYear() {
        assertTrue(leapYear.isLeapYear(2024));
    }

    @Test
    public void testNonLeapYear() {
        assertFalse(leapYear.isLeapYear(2023));
    }

    @Test
    public void testCenturyNonLeapYear() {
        assertFalse(leapYear.isLeapYear(1900));
    }

    @Test
    public void testCenturyLeapYear() {
        assertTrue(leapYear.isLeapYear(2000));
    }
}
Step 7: Run JUnit Tests in IntelliJ
Open LeapYearTest.java.
Right-click inside the file.
Select Run LeapYearTest.
Verify the test results.
Expected output:
Tests passed: 4
Failures: 0
Errors: 0
Step 8: Run Maven Build
Open the IntelliJ Terminal and execute:
mvn clean test
Expected output:
BUILD SUCCESS
Generate the JAR:
mvn clean package
Generated JAR location:
target/LeapYearApp-1.0-SNAPSHOT.jar
Step 9: Create Azure Pipeline YAML
Create a new file named:
azure-pipelines.yml
Location: Project root (same location as pom.xml).
trigger:
- main

pool:
  vmImage: ubuntu-latest

steps:

- task: JavaToolInstaller@0
  inputs:
    versionSpec: '17'
    jdkArchitectureOption: 'x64'
    jdkSourceOption: 'PreInstalled'
  displayName: 'Install Java 17'

- script: |
    java -version
    mvn -version
    mvn clean test
  displayName: 'Build and Run Regression Tests'

- script: mvn clean package
  displayName: 'Generate JAR Artifact'

- task: PublishBuildArtifacts@1
  inputs:
    PathtoPublish: 'target'
    ArtifactName: 'LeapYear-JAR'
    publishLocation: 'Container'
  displayName: 'Publish JAR Artifact'
Step 10: Upload Project to GitHub
Create a GitHub repository named LeapYearApp.
Open the IntelliJ Terminal:
git init
git add .
git commit -m "Leap year Maven application with JUnit tests"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/LeapYearApp.git
git push -u origin main
Replace YOUR_USERNAME with your GitHub username.
Step 11: Create Azure Pipeline
Open Azure DevOps.
Sign in to your organization.
Open your project.
Go to Pipelines → New Pipeline.
Select GitHub.
Authorize Azure DevOps.
Select the LeapYearApp repository.
Choose Existing Azure Pipelines YAML file.
Select branch main.
Choose /azure-pipelines.yml.
Click Run.
Step 12: Verify Pipeline Execution
The Azure Pipeline performs:
Install Java 17.
Compile Java source code.
Run JUnit regression tests.
Generate JAR artifact.
Publish the artifact.
Expected result:
BUILD SUCCESS

Tests run: 4
Failures: 0
Errors: 0
Step 13: Download the JAR Artifact
Open the successful pipeline run.
Go to Summary.
Locate Artifacts.
Click LeapYear-JAR.
Download the artifact.
Generated JAR:
LeapYearApp-1.0-SNAPSHOT.jar
Step 14: Execute the Application (Optional)
java -jar target/LeapYearApp-1.0-SNAPSHOT.jar
Example output:
Enter a year: 2024
2024 is a Leap Year
1           Develop a Java application to calculate the final purchase amount by applying a 10% discount when the purchase amount is ₹1,000 or more; otherwise, no discount is applied. Write JUnit test cases for purchase amounts below, equal to, and above ₹1,000, and configure an Azure Pipeline using Maven to build the application and run the regression tests.
Experiment 8 – Purchase Discount Calculator using Maven, JUnit & Azure Pipeline

Step 1: Create Maven Project in IntelliJ IDEA
Open IntelliJ IDEA.
Click New Project.
Select Maven.
Enter:
Name: DiscountCalculator
JDK: 17
GroupId: org.example
ArtifactId: DiscountCalculator
Click Create.
Step 2: Create Project Structure
DiscountCalculator
│
├── pom.xml
├── azure-pipelines.yml
│
└── src
    ├── main
    │   └── java
    │       └── org
    │           └── example
    │               ├── DiscountCalculator.java
    │               └── Main.java
    │
    └── test
        └── java
            └── org
                └── example
                    └── DiscountCalculatorTest.java
Step 3: Create DiscountCalculator.java
Location: src/main/java/org/example/DiscountCalculator.java
package org.example;

public class DiscountCalculator {

    public double calculateFinalAmount(double amount) {

        if (amount >= 1000) {
            return amount - (amount * 0.10);
        } else {
            return amount;
        }
    }
}
Step 4: Create Main.java
Location: src/main/java/org/example/Main.java
package org.example;

import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter purchase amount: ");
        double amount = sc.nextDouble();

        DiscountCalculator calculator = new DiscountCalculator();

        double finalAmount = calculator.calculateFinalAmount(amount);

        System.out.println("Final Purchase Amount: Rs. " + finalAmount);

        sc.close();
    }
}
Step 5: Configure pom.xml
Location: DiscountCalculator/pom.xml
Replace the contents with:
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         https://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>DiscountCalculator</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.2</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.13.0</version>
            </plugin>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.2.5</version>
            </plugin>

            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-jar-plugin</artifactId>
                <version>3.4.2</version>
                <configuration>
                    <archive>
                        <manifest>
                            <mainClass>org.example.Main</mainClass>
                        </manifest>
                    </archive>
                </configuration>
            </plugin>

        </plugins>
    </build>

</project>
Save the file and reload Maven dependencies.
Step 6: Create JUnit Test Cases
Location: src/test/java/org/example/DiscountCalculatorTest.java
package org.example;

import org.junit.Test;
import static org.junit.Assert.*;

public class DiscountCalculatorTest {

    DiscountCalculator calculator = new DiscountCalculator();

    @Test
    public void testBelow1000() {
        assertEquals(900.0, calculator.calculateFinalAmount(900), 0.001);
    }

    @Test
    public void testEqualTo1000() {
        assertEquals(900.0, calculator.calculateFinalAmount(1000), 0.001);
    }

    @Test
    public void testAbove1000() {
        assertEquals(1800.0, calculator.calculateFinalAmount(2000), 0.001);
    }
}
Step 7: Run JUnit Tests in IntelliJ
Open DiscountCalculatorTest.java.
Right-click inside the file.
Click Run DiscountCalculatorTest.
Verify the test results.
Expected output:
Tests passed: 3
Failures: 0
Errors: 0
Step 8: Run Maven Build
Open the IntelliJ Terminal and execute:
mvn clean test
Expected:
BUILD SUCCESS
Generate the JAR:
mvn clean package
Generated JAR location:
target/DiscountCalculator-1.0-SNAPSHOT.jar
Step 9: Create Azure Pipeline YAML
Create a new file named azure-pipelines.yml in the project root, beside pom.xml.
Location: DiscountCalculator/azure-pipelines.yml
trigger:
- main

pool:
  vmImage: ubuntu-latest

steps:

- task: JavaToolInstaller@0
  inputs:
    versionSpec: '17'
    jdkArchitectureOption: 'x64'
    jdkSourceOption: 'PreInstalled'
  displayName: 'Install Java 17'

- script: |
    java -version
    mvn -version
    mvn clean test
  displayName: 'Build and Run Regression Tests'

- script: mvn clean package
  displayName: 'Generate JAR Artifact'

- task: PublishBuildArtifacts@1
  inputs:
    PathtoPublish: 'target'
    ArtifactName: 'DiscountCalculator-JAR'
    publishLocation: 'Container'
  displayName: 'Publish JAR Artifact'
Step 10: Upload Project to GitHub
Create a GitHub repository named DiscountCalculator.
Open the IntelliJ Terminal:
git init
git add .
git commit -m "Discount calculator Maven project with JUnit tests"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/DiscountCalculator.git
git push -u origin main
Replace YOUR_USERNAME with your GitHub username.
Step 11: Create Azure Pipeline
Open Azure DevOps.
Sign in to your organization.
Open your project.
Navigate to Pipelines → New Pipeline.
Select GitHub.
Authorize Azure DevOps if prompted.
Select the DiscountCalculator repository.
Choose Existing Azure Pipelines YAML file.
Select branch main.
Select /azure-pipelines.yml.
Click Run.
Step 12: Verify Pipeline Execution
The pipeline performs the following steps:
Install Java 17.
Compile the Java application.
Run JUnit regression tests.
Generate the JAR artifact.
Publish the artifact.
Expected result:
BUILD SUCCESS

Tests run: 3
Failures: 0
Errors: 0
Step 13: Download the JAR Artifact
Open the successful pipeline run.
Go to Summary.
Locate Artifacts.
Click DiscountCalculator-JAR.
Download the artifact.
Expected JAR:
DiscountCalculator-1.0-SNAPSHOT.jar
Step 14: Execute the Application (Optional)
java -jar target/DiscountCalculator-1.0-SNAPSHOT.jar
Example:
Enter purchase amount: 2000
Final Purchase Amount: Rs. 1800.0




sudo nano /var/lib/jenkins/config.xml
Change user security to false

Execution shell command common:
echo "Compiling Java Program..."
mkdir -p build
         javac -d build src/main/java/org/example/Main.java
         echo "Executing Java Program..."
          echo -e "INPUT" | java -cp build org.example.Main


1           Develop a Java application to calculate and display the gross salary of an employee based on the basic salary, House Rent Allowance (HRA), and Dearness Allowance (DA) provided as input, using the formula Gross Salary = Basic Salary + HRA + DA. Install and configure Jenkins on a cloud virtual machine, configure Java, and create a Jenkins job to compile and execute the application.
Experiment 1 – Gross Salary Calculation using Java & Jenkins
Step 1: Start Jenkins on Linux
Open the Linux terminal:
sudo systemctl start jenkins
Check whether Jenkins is running:
sudo systemctl status jenkins
If it shows active (running), Jenkins is ready.
Open Jenkins in your browser:
http://localhost:8080
If Jenkins requires the initial password:
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
Step 2: Create Java Project in IntelliJ IDEA
Open IntelliJ IDEA.
Click New Project.
Select Java.
Project name: GrossSalary
Select JDK 17.
Click Create.
Project structure:
GrossSalary
└── src
    └── Main.java
Step 3: Write Java Program
Create Main.java inside the src folder.
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter Basic Salary: ");
        double basic = sc.nextDouble();

        System.out.print("Enter HRA: ");
        double hra = sc.nextDouble();

        System.out.print("Enter DA: ");
        double da = sc.nextDouble();

        double grossSalary = basic + hra + da;

        System.out.println("Gross Salary: " + grossSalary);

        sc.close();
    }
}
Step 4: Run in IntelliJ IDEA
Open Main.java.
Click the green ▶ Run button beside main().
Enter the values in the Run console.
Example:
Enter Basic Salary: 25000
Enter HRA: 5000
Enter DA: 3000
Gross Salary: 33000.0
Step 5: Upload the Project to GitHub
Create a GitHub repository called GrossSalary.
Open the IntelliJ terminal:
git init
git add .
git commit -m "Gross salary Java application"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/GrossSalary.git
git push -u origin main
Replace YOUR_USERNAME with your GitHub username.
Step 6: Create Jenkins Job
Open Jenkins at http://localhost:8080.
Click New Item.
Enter the job name GrossSalaryJob.
Select Freestyle project.
Click OK.
Step 7: Configure GitHub Source Code
Under Source Code Management:
Select Git.
Repository URL:
https://github.com/YOUR_USERNAME/GrossSalary.git
3. Branch:
*/main
Step 8: Configure Build Step
Under Build Steps:
Click Add build step.
Select Execute shell.
Enter:
mkdir -p build
javac -d build src/main/java/org/example/Main.java
echo "25000
5000
3000" | java -cp build org.example.Main

4. Click Save.
Step 9: Build the Jenkins Job
Open GrossSalaryJob.
Click Build Now.
Wait for the build to complete.
Click the build number.
Open Console Output.

CI
1           Develop a Java application to calculate the factorial of a non-negative integer using a loop. Create a Jenkins CI pipeline with stages for checking out the source code from GitHub, compiling the program, and executing it.
Experiment 13: Factorial Calculation Using Java and Jenkins CI Pipeline
Step 1: Create a Java Project in IntelliJ IDEA
Open IntelliJ IDEA.
Click New Project.
Select Java.
Enter project name: factorial.
Select JDK 17.
Select Build System: IntelliJ.
Click Create.
Your project structure will be:
factorial/
├── .idea/
├── src/
│   └── Main.java
├── .gitignore
└── factorial.iml
Important: We will use this exact structure. Do not create a package or additional main/java directories.
Step 2: Write the Java Program
Open src/Main.java and replace its contents with:
Main.java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter a non-negative integer: ");
        int num = sc.nextInt();

        if (num < 0) {
            System.out.println("Factorial is not defined for negative numbers.");
        } else {
            long factorial = 1;

            for (int i = 1; i <= num; i++) {
                factorial = factorial * i;
            }

            System.out.println("Factorial of " + num + " is " + factorial);
        }

        sc.close();
    }
}
Step 3: Execute the Java Program in IntelliJ
Open Main.java.
Click the green Run button beside main().
Enter the input:
5
Expected output:
Enter a non-negative integer: 5
Factorial of 5 is 120
Test additional inputs:
Input
Expected output
0
Factorial of 0 is 1
4
Factorial of 4 is 24
5
Factorial of 5 is 120
-3
Factorial is not defined for negative numbers.

Note: The long data type can store factorials up to 20! without overflow.
Step 4: Create a GitHub Repository
Open GitHub.
Log in to your account.
Click the + icon in the top-right corner.
Select New repository.
Enter repository name:
Factorial

Select Public.
Click Create repository.
Step 5: Push the Java Project to GitHub
Open the IntelliJ terminal.
Make sure you are in the project root directory:
C:\Users\SRIJAA\IdeaProjects\factorial
Execute the following commands one by one.
1. Initialize Git
git init
2. Add the Java source file
git add src/Main.java
3. Commit the source code
git commit -m "Factorial Java application"
4. Set the branch name
git branch -M main
5. Connect the GitHub repository
git remote add origin https://github.com/YOUR_USERNAME/Factorial.git
Replace YOUR_USERNAME with your GitHub username.
6. Push the source code
git push -u origin main
Open your GitHub repository and verify that src/Main.java is uploaded.
Step 6: Create the Jenkinsfile
Return to IntelliJ IDEA.
Right-click the project root folder factorial.
Select New → File.
Enter the filename:
Jenkinsfile
5. Paste the following pipeline code.
Jenkinsfile
pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code from GitHub'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Compiling Java Program'

                sh '''
                    mkdir -p build
                    javac -d build src/Main.java
                '''
            }
        }

        stage('Execute') {
            steps {
                echo 'Executing Factorial Program'

                sh '''
                    echo "5" | java -cp build Main
                '''
            }
        }
    }
}
Explanation of Jenkins stages
Stage
Description
Checkout
Fetches the source code from GitHub
Build
Compiles Main.java using the Java compiler
Execute
Executes the compiled Java program with input 5

Step 7: Push Jenkinsfile to GitHub
Open the IntelliJ terminal and execute:
git add Jenkinsfile

git commit -m "Add Jenkins CI pipeline"

git push origin main
Your final project structure will be:
factorial/
├── .idea/
├── src/
│   └── Main.java
├── Jenkinsfile
├── .gitignore
└── factorial.iml
Your GitHub repository should contain both Main.java and Jenkinsfile.
Step 8: Start Jenkins
Since Jenkins is installed in your Ubuntu environment, open the Ubuntu terminal.
Start Jenkins:
sudo systemctl start jenkins
Check Jenkins status:
sudo systemctl status jenkins
Open the browser:
http://localhost:8080
Log in to Jenkins.
Step 9: Create a Jenkins Pipeline Job
Open the Jenkins dashboard.
Click New Item.
Enter the job name:
FactorialPipeline

Select Pipeline.
Click OK.
Step 10: Configure GitHub Source Code Checkout
Scroll down to the Pipeline section.
Select and enter the following details:
Field
Configuration
Definition
Pipeline script from SCM
SCM
Git
Repository URL
https://github.com/YOUR_USERNAME/Factorial.git
Credentials
None (for public repository)
Branch Specifier
*/main
Script Path
Jenkinsfile

Click Save.
Automating CI/CD and GitOps with Jenkins | Red Hat Developer
Step 11: Execute the Jenkins Pipeline
Open the FactorialPipeline job.
Click Build Now.
Wait for the pipeline to complete.
Click the latest build number.
Select Console Output.
Expected output:
Checking out source code from GitHub

Compiling Java Program

Executing Factorial Program

Enter a non-negative integer: 5
Factorial of 5 is 120

Finished: SUCCESS
Step 12: Configure Automatic Build Trigger
To trigger a new build whenever the GitHub source code is updated:
Open the FactorialPipeline job.
Click Configure.
Find the Build Triggers section.
Select Poll SCM.
Enter the following schedule:
H/2 * * * *
6. Click Save.
Jenkins will check the GitHub repository approximately every two minutes and trigger a new build when it detects a change.
Step 13: Test Automatic Build Triggering
Open Main.java in IntelliJ.
Modify the output message slightly.
Save the file.
Open the IntelliJ terminal.
Push the updated source code:
git add .
git commit -m "Update factorial program"
git push origin main

Wait for Jenkins to detect the update.
Open the Jenkins dashboard.
Verify that a new build has started automatically.
Step 14: Verify Jenkins Pipeline Stages
The Jenkins Stage View should show three successful stages:
FactorialPipeline
Checkout
Success
Build
Success
Execute
Success
Important: Jenkins Environment
Your Java project is created on Windows, but Jenkins is running on Ubuntu/WSL.
Therefore:
Push your project from Windows IntelliJ to GitHub.
Jenkins checks out the project from GitHub into its own workspace.
Jenkins executes the sh commands on Ubuntu.
Ensure Java JDK is installed and java and javac are available to the Jenkins service.
If Jenkins reports javac: not found, configure the JDK in the Jenkins environment before running the pipeline.




1           Develop a Java application to determine whether a given integer reads the same forwards and backwards. Configure a Jenkins Continuous Integration (CI) pipeline to retrieve the source code from GitHub, compile the program, and execute it.

package org.example;
import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter an integer: ");
        int num = sc.nextInt();
        int original = num;
        int reversed = 0;
        while (num > 0) {
            int digit = num % 10;
            reversed = reversed * 10 + digit;
            num = num / 10;
        }
        if (original == reversed) {
            System.out.println(original + " is a Palindrome");
        } else {
            System.out.println(original + " is not a Palindrome");
        }
        sc.close();
    }
}
 
1           Develop a Java application to determine whether a given integer is a prime number. Configure a Jenkins CI pipeline with source code checkout and build stages, and trigger a new build whenever the source code is updated in GitHub.

package org.example;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        System.out.print("Enter an integer: ");
        int num = sc.nextInt();

        boolean isPrime = true;

        if (num <= 1) {
            isPrime = false;
        } else {
            for (int i = 2; i <= Math.sqrt(num); i++) {
                if (num % i == 0) {
                    isPrime = false;
                    break;
                }
            }
        }

        if (isPrime) {
            System.out.println(num + " is a Prime Number");
        } else {
            System.out.println(num + " is not a Prime Number");
        }

        sc.close();
    }
}


 
1           Develop a Java application to read five integers into an array and calculate their sum. Configure a Jenkins CD pipeline to build the application, generate the JAR file, deploy it to a separate deployment directory on the local machine, and execute the deployed application.
package org.example;
import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
 Scanner sc = new Scanner(System.in);
        int[] arr = new int[5];
        int sum = 0;
        System.out.println("Enter five integers:");
        for (int i = 0; i < 5; i++) {
            arr[i] = sc.nextInt();
            sum += arr[i];
        }
        System.out.println("Sum of five integers = " + sum);
   	   sc.close();
    }
}






1           Develop a Java application to calculate simple interest using the principal amount, rate of interest, and time period provided as input. Create a Gradle Java project, configure the build.gradle file, and build the application to generate the required build artifacts.
Experiment: Simple Interest Calculation Using Java and Gradle
Aim
To develop a Java application to calculate Simple Interest using the principal amount, rate of interest, and time period provided as input. Create a Gradle Java project, configure the build.gradle file, compile the source code, and package the application into an executable JAR file.
Step 1: Install Gradle
Open the Ubuntu terminal (WSL) and execute:
sudo snap install gradle --classic
Verify Gradle installation:
gradle --version
Expected: Gradle version 8.14.6 or another installed version.
Step 2: Check Java Installation
Execute:
java -version

javac -version
Ensure Java JDK is installed. The instructions below use Java 21.
Step 3: Create a Project Directory
mkdir java_application
Navigate into the directory:
cd java_application
Step 4: Initialize the Gradle Project
Execute:
gradle init
Select the following options when prompted:
Gradle prompt
Selection
Project type
1 – Application
Implementation language
1 – Java
Target Java version
17
Project name
java_application
Application structure
1 – Single application project
Build script DSL
2 – Groovy
Test framework
1 – JUnit 4
Generate build using new APIs
No

Note: Select Groovy so that the project generates build.gradle instead of build.gradle.kts.
Step 5: Install Tree Utility
Install the tree command to view the project structure:
sudo apt install tree -y
Display the project structure:
tree -L 4
Your generated project will have this structure:
java_application/
├── app/
│   ├── build.gradle
│   └── src/
│       ├── main/
│       │   └── java/
│       │       └── org/
│       │           └── example/
│       │               └── App.java
│       └── test/
├── gradle/
├── gradlew
├── gradlew.bat
├── gradle.properties
└── settings.gradle
Important: Since you selected Single application project, the Java source and build configuration are inside the app directory. The root directory does not need a build.gradle file.
Step 6: Run the Default Gradle Application
Make sure you are in the project root:
cd ~/java_application
Execute:
./gradlew run
The default application should display:
Hello World!
Step 7: Navigate to the Java Source Directory
Navigate to:
cd ~/java_application/app/src/main/java/org/example
List the files:
ls
You should see:
App.java
Open the file:
nano App.java
Step 8: Write the Simple Interest Java Program
Replace the existing code with:
App.java
package org.example;

import java.util.Scanner;

public class App {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter Principal Amount: ");
        double principal = sc.nextDouble();

        System.out.print("Enter Rate of Interest: ");
        double rate = sc.nextDouble();

        System.out.print("Enter Time (in years): ");
        double time = sc.nextDouble();

        double simpleInterest = (principal * rate * time) / 100;

        System.out.println("Simple Interest = " + simpleInterest);

        sc.close();
    }
}
Save the file:
Press Ctrl + O.
Press Enter.
Press Ctrl + X.
Step 9: Configure the app/build.gradle File
Navigate to the application directory:
cd ~/java_application/app
Open the Gradle configuration:
nano build.gradle
Replace its contents with:
app/build.gradle
plugins {
    id 'application'
}

repositories {
    mavenCentral()
}

application {
    mainClass = 'org.example.App'
}

tasks.named('run') {
    standardInput = System.in
}

tasks.jar {
    manifest {
        attributes(
            'Main-Class': 'org.example.App'
        )
    }
}
Save the file.
Important configurations:
application specifies the main Java class.
standardInput = System.in enables Scanner input when running through Gradle.
Main-Class specifies the entry point in the JAR manifest, allowing the JAR to execute using java -jar.
Step 10: Return to the Project Root
cd ~/java_application
Always execute the following Gradle Wrapper commands from this root directory.
Step 11: Run the Simple Interest Application
Execute:
./gradlew run
Enter the following values:
Sample Input
Enter Principal Amount: 10000
Enter Rate of Interest: 5
Enter Time (in years): 2
Expected Output
Simple Interest = 1000.0
If the program accepts input and displays the correct result, the application is working.
Step 12: Build the Gradle Project
Execute:
./gradlew clean build
This command:
Removes previous build files.
Compiles the Java source code.
Compiles and executes the tests.
Generates the build artifacts.
Expected output:
BUILD SUCCESSFUL
Step 13: Generate the Executable JAR File
Execute:
./gradlew :app:jar
Expected output:
BUILD SUCCESSFUL
Step 14: Verify the Generated JAR
Navigate to the generated JAR directory:
ls app/build/libs/
Expected output:
app.jar
The complete JAR path is:
app/build/libs/app.jar
Step 15: Verify the JAR Manifest
This step ensures that the JAR contains the main class configuration.
Execute:
unzip -p app/build/libs/app.jar META-INF/MANIFEST.MF
Expected output:
Manifest-Version: 1.0
Main-Class: org.example.App
If Main-Class is missing, check the tasks.jar configuration in app/build.gradle and rebuild.
Step 16: Execute the Generated JAR
Execute:
java -jar app/build/libs/app.jar
Enter:
10000
5
2
Expected output:
Enter Principal Amount: 10000
Enter Rate of Interest: 5
Enter Time (in years): 2
Simple Interest = 1000.0
JAR execution successful
Step 17: Verify the Complete Project Structure
Return to the project root:
cd ~/java_application
Execute:
tree -L 6
Expected important structure:
java_application/
├── app/
│   ├── build/
│   │   ├── classes/
│   │   ├── generated/
│   │   ├── libs/
│   │   │   └── app.jar
│   │   └── tmp/
│   ├── build.gradle
│   └── src/
│       ├── main/
│       │   └── java/
│       │       └── org/
│       │           └── example/
│       │               └── App.java
│       └── test/
├── gradle/
├── gradlew
├── gradlew.bat
├── gradle.properties
└── settings.gradle
Important Commands for the Practical
Operation
Command
Check Gradle version
gradle --version
Initialize project
gradle init
Run application
./gradlew run
Build project
./gradlew clean build
Generate JAR
./gradlew :app:jar
View build files
tree app/build
List JAR files
ls app/build/libs/
Check manifest
unzip -p app/build/libs/app.jar META-INF/MANIFEST.MF
Execute JAR
java -jar app/build/libs/app.jar

 
1           Develop a Java application to read an English alphabet character and determine whether it is a vowel or a consonant. Create a Gradle Java project, configure the build script, and compile and package the application into a JAR file.

package org.example;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);

        System.out.print("Enter an English alphabet character: ");
        char ch = sc.next().charAt(0);

     
            ch = Character.toLowerCase(ch);

            if (ch == 'a' || ch == 'e' || ch == 'i' ||
                ch == 'o' || ch == 'u') {
                System.out.println(ch + " is a Vowel");
            } else {
                System.out.println(ch + " is a Consonant");
            }
        

        sc.close();
    }
}



Installation of ansible

Experiment: Installation and Configuration of Ansible on Ubuntu Linux
Step 1: Open Ubuntu Terminal
Open your Ubuntu terminal (WSL).
Update the package repository:
sudo apt update
Step 2: Install Software Properties Common
Execute:
sudo apt install software-properties-common -y
Step 3: Add Ansible PPA
Add the official Ansible repository:
sudo add-apt-repository --yes --update ppa:ansible/ansible
Step 4: Install Ansible
Execute:
sudo apt install ansible -y
Wait until the installation is completed.
Step 5: Verify Ansible Installation
Check the installed Ansible version:
ansible --version
Expected output (version may differ):
ansible [core 2.x.x]
  config file = None
  python version = 3.x.x
Step 6: Check Ansible Galaxy
Verify that Ansible Galaxy is installed:
ansible-galaxy --version
Step 7: Check Ansible Configuration
Display the default Ansible configuration:
ansible-config list
Step 8: Test Ansible Connectivity with Localhost
Execute:
ansible localhost -m ping -c local
Expected output:
localhost | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
Step 9: Check Python Installation
Ansible requires Python.
Verify Python:
python3 --version
Step 10: Verify Locale Configuration
Check the locale:
locale
Ansible requires UTF-8 encoding.
If the locale is not UTF-8, execute:
sudo apt install locales -y
sudo locale-gen en_US.UTF-8
sudo update-locale LANG=en_US.UTF-8
Close and reopen the terminal, then verify:
locale
Important Commands
Operation
Command
Update packages
sudo apt update
Install Ansible repository support
sudo apt install software-properties-common -y
Add Ansible PPA
sudo add-apt-repository --yes --update ppa:ansible/ansible
Install Ansible
sudo apt install ansible -y
Check Ansible version
ansible --version
Check Galaxy version
ansible-galaxy --version
Test localhost
ansible localhost -m ping -c local
Check Python
python3 --version

Note: Ansible does not require starting a service. Once installed, it can be used directly from the terminal.

Experiment: Install Git, PostgreSQL and Apache Using Ansible Roles
Aim
To use Ansible on a Linux system and create three Ansible roles named prerequisites, PostgreSQL, and apache to install Git, PostgreSQL, and Apache web server, respectively. Create a stack.yml playbook to execute all three roles on localhost and verify the successful installation of the required packages.
Step 1: Open Ubuntu Terminal
Since Ansible is already installed on your Ubuntu system (WSL), you do not need to install it again.
Open Ubuntu terminal and check the Ansible version:
ansible --version
Expected output will display the installed Ansible version, configuration file location, Python version and other details.
Step 2: Check Ansible Installation
Check whether Ansible can communicate with localhost:
ansible localhost -m ping -c local
Expected output:
localhost | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
Important: Ansible is an agentless automation tool. It does not run as a background service like Jenkins or Apache. You do not need to start an Ansible service. You execute Ansible commands and playbooks directly from the terminal.
Step 3: Check the Locale Configuration
Ansible requires UTF-8 locale encoding.
Check the current locale:
locale
If the output shows UTF-8 encoding, continue.
If it shows ISO8859-1 or another non-UTF-8 encoding, execute:
sudo update-locale LANG=en_US.UTF-8
Then close and reopen the Ubuntu terminal.
Verify:
locale
Step 4: Create a Project Directory
Create a directory named ansible_roles:
mkdir ansible_roles
Navigate into it:
cd ansible_roles
Step 5: Create the Three Ansible Roles
Use the ansible-galaxy init command to generate the role directory structures.
Create the prerequisites role:
ansible-galaxy init prerequisites
Create the PostgreSQL role:
ansible-galaxy init PostgreSQL
Create the Apache role:
ansible-galaxy init apache
These commands generate the standard directory structure for each role.
Step 6: Verify the Role Directories
Execute:
tree
The important directories should look like:
ansible_roles/
├── prerequisites/
│   ├── tasks/
│   │   └── main.yml
│   ├── handlers/
│   ├── defaults/
│   ├── vars/
│   ├── files/
│   └── templates/
├── PostgreSQL/
│   ├── tasks/
│   │   └── main.yml
│   ├── handlers/
│   ├── defaults/
│   ├── vars/
│   ├── files/
│   └── templates/
└── apache/
    ├── tasks/
    │   └── main.yml
    ├── handlers/
    ├── defaults/
    ├── vars/
    ├── files/
    └── templates/
Each role contains a tasks/main.yml file where the installation tasks will be defined.
Step 7: Organize Roles Inside a roles Directory
Ansible playbooks automatically search for roles in a directory named roles relative to the playbook.
If you created the three roles directly inside ansible_roles, move them into roles:
mkdir roles
mv prerequisites PostgreSQL apache roles/
Your structure should now be:
ansible_roles/
└── roles/
    ├── prerequisites/
    ├── PostgreSQL/
    └── apache/
Step 8: Configure the Prerequisites Role
The prerequisites role is responsible for installing Git.
Navigate to its tasks directory:
nano roles/prerequisites/tasks/main.yml
Replace the contents with:
roles/prerequisites/tasks/main.yml
---
- name: Update package repository
  apt:
    update_cache: yes

- name: Install Git
  apt:
    name: git
    state: present
Save the file using Ctrl + O, Enter and Ctrl + X.
Step 9: Configure the PostgreSQL Role
Navigate to the PostgreSQL tasks directory:
nano roles/PostgreSQL/tasks/main.yml
Replace the contents with:
roles/PostgreSQL/tasks/main.yml
---
- name: Install PostgreSQL
  apt:
    name: postgresql
    state: present
    update_cache: yes

- name: Start and enable PostgreSQL service
  service:
    name: postgresql
    state: started
    enabled: yes
Save the file.
Step 10: Configure the Apache Role
Navigate to the Apache tasks directory:
nano roles/apache/tasks/main.yml
Replace the contents with:
roles/apache/tasks/main.yml
---
- name: Install Apache web server
  apt:
    name: apache2
    state: present
    update_cache: yes

- name: Start and enable Apache service
  service:
    name: apache2
    state: started
    enabled: yes
Save the file.
Step 11: Create the stack.yml Playbook
Return to the project root:
cd ~/ansible_roles
Create the playbook:
nano stack.yml
Enter the following code:
stack.yml
---
- name: Install Git, PostgreSQL and Apache
  hosts: localhost
  connection: local
  become: yes

  roles:
    - prerequisites
    - PostgreSQL
    - apache
Save the file.
Explanation
Configuration
Purpose
hosts: localhost
Executes the playbook on the local machine
connection: local
Uses a local connection
become: yes
Executes tasks with administrator privileges
roles
Specifies the three roles to execute
prerequisites
Installs Git
PostgreSQL
Installs PostgreSQL
apache
Installs Apache web server

Step 12: Verify the Project Structure
Execute:
tree
Expected structure:
ansible_roles/
├── roles/
│   ├── prerequisites/
│   │   └── tasks/
│   │       └── main.yml
│   ├── PostgreSQL/
│   │   └── tasks/
│   │       └── main.yml
│   └── apache/
│       └── tasks/
│           └── main.yml
└── stack.yml
Step 13: Check the Playbook Syntax
Before executing, verify the YAML syntax:
ansible-playbook stack.yml --syntax-check
Expected output:
playbook: stack.yml
Step 14: Execute the Ansible Playbook
Run:
ansible-playbook -i localhost, -c local stack.yml --ask-become-pass
Enter your Ubuntu sudo password when prompted.
Ansible will execute the three roles in sequence:
Install Git.
Install PostgreSQL.
Install Apache web server.
Expected output will show tasks similar to:
TASK [prerequisites : Update package repository] ********
changed: [localhost]

TASK [prerequisites : Install Git] ***********************
changed: [localhost]

TASK [PostgreSQL : Install PostgreSQL] *******************
changed: [localhost]

TASK [PostgreSQL : Start and enable PostgreSQL service] **
changed: [localhost]

TASK [apache : Install Apache web server] ****************
changed: [localhost]

TASK [apache : Start and enable Apache service] **********
changed: [localhost]

PLAY RECAP ************************************************
localhost : ok=6 changed=6 unreachable=0 failed=0
Actual task counts and changed values may vary depending on which packages are already installed.
Step 15: Verify Git Installation
Execute:
git --version
Expected output:
git version 2.x.x
Step 16: Verify PostgreSQL Installation
Check PostgreSQL version:
psql --version
Check its service:
sudo service postgresql status
Expected status:
Active: active (exited)
or another active status depending on the Ubuntu service configuration.
Step 17: Verify Apache Installation
Check Apache version:
apache2 -v
Check Apache service:
sudo service apache2 status
Expected status:
Active: active (running)
Step 18: Verify Apache Web Server
Open a browser and enter:
http://localhost
You should see the Apache2 Ubuntu Default Page.
Running Multiple PHP Instances with LAMP Stack on Ubuntu/Kubuntu 23.10 Linux 2024 (Update 2026)
phoca.cz
Alternatively, verify through the terminal:
curl http://localhost
The output should contain the Apache default page HTML.
Important Commands for the Practical
Operation
Command
Check Ansible version
ansible --version
Test localhost
ansible localhost -m ping -c local
Create a role
ansible-galaxy init ROLE_NAME
View directory structure
tree
Check playbook syntax
ansible-playbook stack.yml --syntax-check
Execute playbook
ansible-playbook -i localhost, -c local stack.yml --ask-become-pass
Check Git
git --version
Check PostgreSQL
psql --version
Check Apache
apache2 -v
Check Apache service
sudo service apache2 status

Result
Ansible was used to create three roles: prerequisites, PostgreSQL, and apache. The stack.yml playbook was configured and executed successfully on localhost. Git, PostgreSQL, and Apache web server were installed, and their installations were verified successfully.

Experiment 26: Create an Ansible playbook for a simple application and use modules in Ansible
We will perform this experiment in Ubuntu on WSL, using your existing Ansible installation.
We will create a simple web application deployment playbook that uses Ansible modules to:
Update the Ubuntu package repository.
Install Apache web server.
Start and enable Apache.
Create an application directory.
Deploy a sample HTML webpage.
Verify that the application is running.
Practical experiment
Step 1: Check Ansible installation
Open Ubuntu terminal and execute:
ansible --version
Check whether Apache is already installed:
apache2 -v
If Apache is not installed, that is fine. The playbook will install it.
Step 2: Create the project directory
mkdir -p ~/ansible_app
cd ~/ansible_app
Create the playbook:
nano app.yml
Step 3: Write the Ansible playbook
Enter the following code in app.yml.

---
- name: Deploy a Simple Web Application
  hosts: localhost
  connection: local
  become: yes
  gather_facts: no

  tasks:

    - name: Update package repository
      apt:
        update_cache: yes

    - name: Install Apache web server
      apt:
        name: apache2
        state: present

    - name: Start and enable Apache
      service:
        name: apache2
        state: started
        enabled: yes

    - name: Create application directory
      file:
        path: /var/www/html/myapp
        state: directory
        mode: '0755'

    - name: Deploy application webpage
      copy:
        dest: /var/www/html/myapp/index.html
        content: |
          <html>
          <head>
              <title>My Ansible Application</title>
          </head>
          <body>
              <h1>Welcome to My Application!</h1>
              <p>Successfully deployed using Ansible.</p>
          </body>
          </html>
        mode: '0644'

    - name: Verify application deployment
      command: cat /var/www/html/myapp/index.html
      register: app_output
      changed_when: false

    - name: Display deployment result
      debug:
        msg: "Application deployed successfully!"
Save the file using Ctrl + O, Enter, and Ctrl + X.
Step 4: Check playbook syntax
Before executing, check for YAML errors:
ansible-playbook app.yml --syntax-check
Expected output:
playbook: app.yml
Step 5: Execute the playbook
Run:
ansible-playbook -i localhost, -c local app.yml -K
Enter your Ubuntu password when prompted at BECOME password:.
The playbook will execute all seven tasks.
Expected output will look similar to:
PLAY [Deploy a Simple Web Application]

TASK [Update package repository] ************************* ok
TASK [Install Apache web server] ************************ changed
TASK [Start and enable Apache] *************************** changed
TASK [Create application directory] ********************** changed
TASK [Deploy application webpage] ************************ changed
TASK [Verify application deployment] ********************* ok
TASK [Display deployment result] ************************ ok

PLAY RECAP
localhost : ok=7 changed=5 unreachable=0 failed=0
The number of changed tasks may differ if Apache or the application files already exist.
If the same sudo timeout occurs: Stop and share the output rather than changing sudoers. Your earlier tests showed that normal sudo works, but Ansible's password handling still needs to be verified.
Step 6: Verify Apache service
Check whether Apache is running:
sudo service apache2 status
Expected:
Active: active (running)
Step 7: Verify the deployed application
Execute:
curl http://localhost/myapp/
Expected HTML output:
<html>
<head>
    <title>My Ansible Application</title>
</head>
<body>
    <h1>Welcome to My Application!</h1>
    <p>Successfully deployed using Ansible.</p>
</body>
</html>
You can also open this URL in your browser:
http://localhost/myapp/
Running Multiple PHP Instances with LAMP Stack on Ubuntu/Kubuntu 23.10 Linux 2024 (Update 2026)
Step 8: Verify the created files
ls -l /var/www/html/myapp/
Expected:
index.html
View the file:
cat /var/www/html/myapp/index.html
Step 9: Understand the Ansible modules used
Ansible module
Purpose
apt
Installs Apache and updates packages
service
Starts and enables Apache
file
Creates the application directory
copy
Deploys the HTML webpage
command
Executes a Linux command
debug
Displays a success message

Step 10: Important Ansible playbook concepts
Keyword
Explanation
name
Describes the play or task
hosts
Specifies the target machine
connection
Specifies how Ansible connects
become
Executes tasks with administrator privileges
gather_facts
Controls automatic system information collection
tasks
Contains the operations to perform
register
Stores task output in a variable
changed_when
Controls whether a task is reported as changed

Step 11: Experiment result
Result: Thus, an Ansible playbook was successfully created and executed to deploy a simple web application using different Ansible modules such as apt, service, file, copy, command, and debug.
Viva questions
What is Ansible?
Ansible is an open-source automation tool used for configuration management, application deployment, and IT automation.
What is an Ansible playbook?
A playbook is a YAML file containing instructions that Ansible executes on target machines.
What is an Ansible module?
A module is a reusable unit of code that performs a specific task, such as installing software or copying files.
What is the purpose of the apt module?
It manages packages in Debian-based Linux systems.
What is the purpose of the service module?
It manages system services by starting, stopping, restarting, and enabling them.
What is the difference between state: present and state: absent?
present ensures a package or resource exists; absent ensures it is removed.
What is the purpose of become: yes?
It enables privilege escalation to perform administrative operations.
What is YAML?
YAML is a human-readable data serialization format used to write Ansible playbooks.
What is idempotency in Ansible?
Running the same playbook multiple times should maintain the desired state without making unnecessary changes.
How do you execute an Ansible playbook?
ansible-playbook app.yml
For this experiment, because we need administrator privileges:
ansible-playbook -i localhost, -c local app.yml -K


sudo systemctl daemon-reload
sudo systemctl restart jenkins

