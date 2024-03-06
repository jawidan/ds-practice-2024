# OVERVIEW
The Orchestrator service serves as the central coordination point within our microservices architecture, enabling seamless interaction between the frontend, fraud detection, transaction verification, and book suggestion services. By handling requests from the frontend and directing them to the appropriate backend services, it ensures efficient processing of user transactions and enhances the user experience by aggregating responses from various services.

1. There is main _checkout_ function which is responsible for combining 3 microservices into one service and performing user transactions for purchasing books. 

