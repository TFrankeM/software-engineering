<h1 align="center">Software Engineering discipline</h1>

<hr>

<h3> Students responsible for the repository: </h3>

<a href = "https://github.com/G-mikael"> Gerardo Pereira <a/>
<br>
<a href = "https://github.com/TFrankeM"> Thiago Melchiors <a/>
<br>
<a href = "https://github.com/yonirg"> Yonathan Gherman <a/>

<hr>

<h3> Content: </h3>

<h4> Final report A1: </h4>
<p>
    In this <a href="Simulação_de_Sprint_Scrum.pdf">report</a>, we present the decisions made by our team 
    regarding the system's architecture and the application of Extreme Programming (XP) practices as part of the Software Engineering course. This 
    work was conducted during a simulated Scrum sprint, where we prioritized key architectural attributes such as security, stability, and ease of 
    use. Our goal was to align these decisions with the project’s requirements and the specific dynamics of our team. Additionally, we discuss the 
    adoption of XP practices, like Test-Driven Development (TDD) and continuous refactoring, while balancing these with the demands of the project 
    and the team’s unique challenges.
</p>

<h4> Final report A2: </h4>
<p>
    This <a href="Simulação_de_Sprint_Scrum_A2.pdf">report</a> aims to present and justify the design pattern choices adopted by our team in implementing 
    the final version of the project for task A2 of the Software Engineering discipline. Throughout this document, we will detail the design patterns 
    applied to the system, explaining how each one was integrated into the project architecture and the impacts they had on the final implementation. 
    In addition, we will discuss the alternatives that were considered, what the solution would be like without the use of these patterns and the 
    advantages they brought in terms of modularity, maintainability and scalability.
</p>

<h4> Instructions for running the Vending Machine System: </h4>

<p>
  To run the Vending Machine System, follow these steps.
</p>

<h5>Clone the Repository</h5> 
<p>
  First, clone the repository to your local machine using the following command:
</p>

```bash
git clone https://github.com/TFrankeM/software-engineering.git
```

<h5>Install Dependencies</h5> 
<p>
  Navigate to the root of the project directory and install the necessary dependencies. You can use pip to install the required Python packages:
</p>

```bash
pip install pandas bcrypt time sys os sqlite3 datetime uuid unittest
```

<h5>Navigate to the Main File</h5> 
<p>
  Navigate to the directory where the main.py file is located. It's inside the src folder:
</p>

```bash
cd src
```

<h5>Run the Application</h5> 
<p>
  Once you're inside the src folder, you can run the main.py file to start the Vending Machine System:
</p>

```bash
python main.py
```

<h4>Interact with the System</h4> 
<p>
  Follow the on-screen prompts to interact with the vending machine system as an administrator, a seller or a customer. You will be able to:
</p>

<h5>As a User:</h5>
<ul>
  <li>Create an account as a user or seller.</li>
  <li>Alternatively, use pre-existing data in the database (you can find it <a href="Lista clientes vendedores e maquinas.txt">here</a> in the List of <strong>Clients</strong>, <strong>Sellers</strong>, and <strong>Machines</strong>).</li>
  <li>We do not allow the creation of <strong>administrator</strong> accounts due to sensitive matters. However, we provide access to an already created account, with the following credentials:
    <ul>
      <li><strong>Login:</strong> Rafael Pinho</li>
      <li><strong>Password:</strong> (rafa42)</li>
    </ul>
  </li>
</ul>

<h5>As a Seller:</h5>
<ul>
  <li>Create or remove vending machines.</li>
  <li>View and manage all your vending machine empire, with options to:
    <ul>
      <li>Add and remove products.</li>
      <li>Update product information.</li>
    </ul>
  </li>
  <li>Measure how popular your service is with average rating metrics for machines and products.</li>
</ul>

<h5>As an Administrator:</h5>
<ul>
  <li>View problem reports submitted by users.</li>
  <li>Generate basic reports and export them in CSV format.</li>
</ul>

<h5>As a Customer:</h5>
<ul>
  <li>View available vending machines.</li>
  <li>Add machines to your favorites list to receive important notifications.</li>
  <li>View available products in each machine.</li>
  <li>View the product's review history and average rating to know if they are trustworthy.</li>
  <li>Make purchases of multiple products using the shopping cart.</li>
  <li>Add products to your favorites list to receive notifications.</li>
  <li>Receive notifications if your favorite machines are removed from service or if your favorite products are out of stock.</li>
  <li>Write reviews for products and machines.</li>
  <li>Report problems with the app or with machines.</li>
  <li>Top up credit in the system.</li>
</ul>

<hr>

<h4> Stakeholder interview report: </h4>

<p>
  This repository hosts the detailed <a href = "https://tfrankem.github.io/software-engineering/main%20page/index.html">report<a/> on our stakeholder interview activities, carried out 
  within the scope of the study and application of requirements engineering techniques. We plan to 
  include in the   future code snippets of the application addressed during requirements elicitation, 
  which will provide valuable contributions to the study of software engineering.
</p>

<h4> Reflection on practical aircraft production class: </h4>

<p>
  In addition, we incorporated a <a href = "Reflexão_aviões_de_papel.pdf">reflexive analysis<a/> on the production chain dynamics, carried out on 
  September 3, 2024, to enrich our understanding of the process.
</p>
