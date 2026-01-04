This file provides the necessary context for the autonomous coding agent, Jules, to understand the CodeMentor AI platform.
🏗️ Project Overview
CodeMentor AI is an intelligent programming learning platform that integrates artificial intelligence with established educational methods. The system is designed for students, educators, and developers to facilitate effective code learning through AI-driven insights.
📂 Repository Structure
Jules should refer to the following directory structure for task implementation:
• /backend: Core server-side logic, primarily utilizing TypeScript.
• /ai-engine: The AI-focused backend components, written in Python.
• /src & /public: Frontend application files using TypeScript and JavaScript (likely Next.js based on file markers like next.config.js).
• /docs: Comprehensive project documentation, including architecture and API references.
• /monitoring: Configuration for system observability and performance tracking.
• /scripts: Utility scripts for automation and deployment tasks.
🛠️ Technical Stack & Conventions
• Languages: The codebase is composed of TypeScript (40.9%), Python (33.9%), and JavaScript (23.6%).
• Environment Setup: Refer to .env.example for required project configurations. Jules can access project-specific configurations via Environment Variables if they are enabled in the repository settings.
• Containers: Use docker-compose.yml and Dockerfile.frontend for environment initialization and deployment tasks.
• Architecture: Consult archoverview.md for high-level system components and design patterns before suggesting structural changes.
🤖 Instructions for Jules
1. Contextual Awareness: Always check the /docs folder and archoverview.md to ensure new features align with existing service interactions and data flows.
2. Documentation Updates: When implementing new features or fixing bugs, automatically update the relevant documentation in /docs or the main README to maintain 100% documentation coverage.
3. Code Consistency: Maintain strict TypeScript typing in the /backend and follow Pythonic standards in the /ai-engine.
4. Verification: After modifying code, use available test suites (referencing .github/workflows) to verify changes.
5. Memory: Jules should utilize its Memory system to retain preferences and established coding patterns within this repository for long-term project awareness.
🔌 API & Integration
• Project uses OpenAPI/Swagger for API documentation.
• Jules may be tasked with creating custom integrations via the Jules API for CI/CD pipelines or project management tools like Jira/Linear.
