from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Dockerization Summary & Mental Map', 0, 1, 'C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 5, body)
        self.ln()

    def bullet_point(self, text):
        self.set_font('Arial', '', 11)
        self.cell(10) # Indent
        self.cell(5, 5, chr(149), 0, 0) # Bullet
        self.multi_cell(0, 5, text)
        self.ln(2)

pdf = PDF()
pdf.add_page()

# Mental Map Section
pdf.chapter_title('The Mental Map of Dockerizing')
pdf.chapter_body("Think of your project like a Restaurant. Before Docker, you were running everything in your home kitchen (your laptop). Docker lets you package this restaurant so it can be deployed anywhere identically.")

pdf.set_font('Arial', 'B', 11)
pdf.cell(0, 6, "1. The Recipe Card (Dockerfile)", 0, 1)
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 5, "The Dockerfile is the step-by-step recipe to build the kitchen itself.")
pdf.bullet_point("Base Image (FROM python:3.13-slim): We start with a clean, empty kitchen that has Python installed.")
pdf.bullet_point("Ingredients (COPY requirements.txt ...): We buy all the groceries (libraries like Django) and put them in the cupboards.")
pdf.bullet_point("Cookware (RUN apt-get install ...): We install necessary tools (like gcc and mysql clients) to cook the food.")
pdf.bullet_point("The Code (COPY . /app): We bring in your secret family recipes (your source code).")
pdf.bullet_point("The Chef (ENTRYPOINT/CMD): We tell the kitchen what to do when it opens (run migrations, then start the server).")
pdf.ln(2)

pdf.set_font('Arial', 'B', 11)
pdf.cell(0, 6, "2. The Restaurant Manager (docker-compose.yml)", 0, 1)
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 5, "A real restaurant needs more than just a kitchen; it needs a pantry, a freezer, and a cleaning crew. docker-compose manages this team.")
pdf.bullet_point("Web: Your Django app (the Kitchen).")
pdf.bullet_point("DB (MySQL): The Pantry where data lives.")
pdf.bullet_point("Redis: The fast-access Counter/Freezer for catching and quick tasks.")
pdf.bullet_point("Worker: The Cleaning Crew/Prep Cooks (Celery) doing background work.")
pdf.bullet_point("Beat: The Manager who shouts orders at specific times (Scheduled tasks).")
pdf.bullet_point("Networks: The hallways allowing these rooms to talk to each other.")
pdf.ln(2)

pdf.set_font('Arial', 'B', 11)
pdf.cell(0, 6, "3. The Configuration Bridge (prod.py & .env)", 0, 1)
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 5, "Your code needs to know it's not at home anymore.")
pdf.bullet_point("Environment Variables: Instead of hardcoding 'localhost', we use variables like DB_HOST=db. This tells Django: 'The database is in the room named db'.")
pdf.bullet_point("Updates: The 'prod.py' file was modified to allow Django to read these signs posted on the wall by Docker.")
pdf.ln()

# Summary of Changes Section
pdf.chapter_title('Summary of Changes')
pdf.bullet_point("Fixed Missing Dependency: Added 'djoser' to pyproject.toml so the authentication system works.")
pdf.bullet_point("Created Dockerfile: Defines the 'Storefront API' machine.")
pdf.bullet_point("Created docker-compose.yml: Spins up the App, MySQL, Redis, and Celery together.")
pdf.bullet_point("Updated settings/prod.py: Made it flexible to accept configuration from Docker.")
pdf.ln()

pdf.chapter_body("You can now build and run your project using: docker-compose up --build")

pdf.output("Docker_Summary.pdf")
