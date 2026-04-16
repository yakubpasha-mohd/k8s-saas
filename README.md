Full Toolchain in Your Project
🐳 1. Containerization Layer
•	Docker 
•	Docker Compose 
👉 Purpose:
•	Package backend, frontend, and MongoDB into containers 
•	Run everything with one command 
________________________________________
🐍 2. Backend Stack
•	Python 
•	Likely framework (based on structure): 
o	FastAPI or Flask 
👉 Purpose:
•	API layer (/api) 
•	Business logic 
•	AWS integrations 
👉 Runs inside:
backend container (Docker)
________________________________________
🎨 3. Frontend Stack
•	JavaScript 
•	React 
•	Tailwind CSS 
👉 Purpose:
•	UI layer 
•	Talks to backend via HTTP API 
👉 Runs inside:
frontend container (Docker)
________________________________________
🗄 4. Database
•	MongoDB 
👉 Purpose:
•	Stores application data 
👉 Runs inside:
mongodb container
________________________________________
☁️ 5. Cloud Layer
•	Amazon EC2 
•	Amazon Web Services 
👉 Purpose:
•	Hosts your entire system 
________________________________________
🔐 6. AWS SDK / Integration
•	Boto3 
👉 Purpose:
•	Backend communicates with AWS services (via keys in .env) 
________________________________________
🧾 7. Environment Config
•	.env file 
👉 Purpose:
•	Store secrets (AWS keys, DB config)
# k8s-saas
