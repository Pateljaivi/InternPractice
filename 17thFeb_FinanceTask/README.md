Personal Finance Tracker API

**Project Overview**

Personal Finance Tracker is a scalable and modular REST API built using FastAPI and MongoDB to efficiently manage income and expense transactions.
The system is designed with clean architecture principles, asynchronous database operations, structured validation, and real-world financial tracking features such as filtering, bulk operations, and monthly summaries.
This project demonstrates backend development best practices including validation, dependency injection, async programming, and aggregation handling.

**Architecture & Design Approach**

The application follows a layered modular architecture:
API Layer – Handles routing and HTTP request/response lifecycle
Schema Layer – Data validation using Pydantic models
Core Layer – Configuration and database connection management
Dependency Layer – Reusable dependencies like pagination
The design ensures:
Separation of concerns
Clean and maintainable code
Scalable structure for future enhancements

**Technical Highlights**

Asynchronous API implementation using FastAPI
Async MongoDB integration via Motor
Structured request validation using Pydantic
Dependency Injection for database handling
MongoDB aggregation for financial summary
Bulk delete operations with date filtering
Query-based filtering (category & date range)
Proper HTTP status codes & exception handling
Environment-based configuration management

**Internal Request Flow**

1.Client Request: User sends an HTTP request.

2.FastAPI Router: Directs the request to the specific endpoint.

3.Pydantic Validation: Validates incoming data against defined schemas.

4.Dependency Injection: Injects required database sessions or pagination logic.

5.Motor Driver: Executes non-blocking queries against MongoDB.

6.Response Serialization: Transforms DB results into structured JSON.

7.Client Response: Delivers the final JSON payload to the user.



**Core Functionalities**

(I)Category Management

Create category
View all categories
Update category
Delete category
Duplicate prevention logic

(II)Transaction Management

Add income/expense transactions
Update transaction details
Delete single transaction
Bulk delete by date range
Filter by category
Filter by date range
Monthly financial summary (Aggregation pipeline)