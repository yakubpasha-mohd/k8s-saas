Full Toolchain Overview

This project is built using a modern, containerized full-stack architecture with cloud integration. Below is a breakdown of the complete toolchain and how each component fits into the system.

🐳 1. Containerization Layer

Technologies:

Docker
Docker Compose

Purpose:

Package backend, frontend, and MongoDB into isolated containers
Enable running the entire application stack with a single command
🐍 2. Backend Stack

Technologies:

Python
FastAPI or Flask (based on project structure)

Purpose:

Provides API layer (/api)
Handles business logic
Manages AWS integrations

Runtime Environment:

Runs inside the backend container (Docker)
🎨 3. Frontend Stack

Technologies:

JavaScript
React
Tailwind CSS

Purpose:

Implements the user interface (UI)
Communicates with backend via HTTP APIs

Runtime Environment:

Runs inside the frontend container (Docker)
🗄 4. Database

Technology:

MongoDB

Purpose:

Stores application data

Runtime Environment:

Runs inside the mongodb container
☁️ 5. Cloud Layer

Technologies:

Amazon EC2
Amazon Web Services (AWS)

Purpose:

Hosts and deploys the entire system
🔐 6. AWS SDK / Integration

Technology:

Boto3

Purpose:

Enables backend communication with AWS services
Uses credentials configured via environment variables
🧾 7. Environment Configuration

Configuration:

.env file

Purpose:

Stores sensitive information such as:
AWS credentials
Database configuration
API keys
⚙️ Running the Project
docker-compose up --build
