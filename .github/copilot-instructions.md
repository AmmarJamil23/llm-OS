Repository Development Protocol

This repository follows a structured AI assisted engineering workflow.

GitHub Copilot must follow the workflow defined in this document whenever assisting with development.

The objective is to produce production grade software systems while training the developer to become:

problem solver
system architect
AI engineer
entrepreneur
product builder
marketer
sales strategist
negotiator

The system must therefore be designed with technical excellence and business awareness.

Copilot must assist not only in writing code but also in improving:

system architecture
product thinking
performance optimization
cost efficiency
user value
business viability

Core Project Vision

The main project built in this repository is an LLM Research Operating System.

This system allows users to:

ingest technical knowledge sources
perform semantic search
run multi agent reasoning
evaluate model performance
conduct AI experiments
visualize retrieval results
analyze system performance

The project must demonstrate practical competence in:

Python software engineering
LLM frameworks and agents
vector databases
NLP embeddings
semantic retrieval
microservices
ML lifecycle
model evaluation
containerized deployment

The system should behave like a technical research assistant platform rather than a simple chatbot.

System Architecture

The platform architecture should resemble production AI systems.

User Interface
↓
Frontend Dashboard
↓
REST API Gateway
↓
Agent Orchestration Layer
↓
Tool Layer
Vector Search
Document Processing
Experiment Runner
Evaluation Engine
↓
Vector Database
↓
LLM Model Runtime
↓
Response and Metrics

Preferred technology stack:

Python
FastAPI
LangGraph
LangChain
FAISS or Chroma
Sentence Transformers
PyTorch
Pandas
NumPy
Ollama with Llama or Mistral models
Docker and Docker Compose
Next.js frontend

All components should run locally and be deployable to cloud environments later.

Development Workflow

Copilot must strictly follow the workflow below.

Code generation must never occur before the research and planning phases are completed.

Phase 1: Research

Before proposing any change or implementation, Copilot must deeply analyze the relevant part of the codebase.

Copilot must:

read the entire relevant folder and related files
understand architecture, dependencies, data flow and conventions
identify design patterns used in the repository
identify constraints and assumptions
identify integration points with other modules

Surface level scanning is not acceptable.

Copilot must deeply understand the code and its intricacies before proceeding.

After completing analysis, Copilot must generate a persistent document:

docs/research.md

The document must contain:

system overview
relevant modules and responsibilities
data flow and control flow
important interfaces and contracts
existing design patterns
potential risks or edge cases
constraints imposed by the system
observations about architecture and performance

The purpose of this document is to create a review surface for the developer.

Copilot must not proceed to planning until the research document exists.

Phase 2: Planning

After the research document is reviewed, Copilot generates an implementation plan.

Copilot must create:

docs/plan.md

The plan must contain:

feature description and business outcome
architecture level approach
step by step implementation strategy
files that will be modified
code snippets showing intended changes
data model changes
API contract changes
dependency updates
migration requirements
testing strategy
performance considerations
tradeoffs and alternatives

Plans must be grounded in the actual codebase.

Hypothetical or generic plans are not acceptable.

Annotation Cycle

The developer may edit plan.md and add comments.

Copilot must:

read the updated document
address every note added by the developer
update the plan accordingly

Copilot must not implement code during this stage.

Implementation begins only after explicit developer approval.

Phase 3: Task Breakdown

Before implementation begins, Copilot must add a detailed task list to plan.md.

Example structure:

Implementation Tasks

Phase 1 Data Model Updates

[ ] modify schema definitions
[ ] update migration scripts
[ ] update ORM models

Phase 2 API Changes

[ ] update service layer
[ ] add new endpoint
[ ] update validation layer

Phase 3 Integration

[ ] integrate frontend
[ ] add tests

The todo list serves as the execution tracker.

Phase 4: Implementation

Implementation begins only when instructed.

Copilot must:

implement all tasks from the plan
mark tasks completed in plan.md
not stop until tasks are finished
follow repository coding conventions

Code generation rules:

avoid unnecessary comments
avoid redundant documentation
avoid unsafe typing
avoid duplicate logic
reuse existing modules when possible

Continuous Verification

During implementation Copilot must:

run type checking
validate imports
verify dependency compatibility
avoid breaking interfaces

Errors must be fixed immediately.

Developer Feedback Loop

Developer corrections may be short and direct.

Examples:

use this library instead
do not change this interface
simplify this logic

Copilot must treat these instructions as authoritative.

If implementation direction becomes incorrect, developer may request reverting changes.

Copilot must comply immediately.

System Modules

The system should eventually include the following modules.

Document ingestion pipeline

Responsible for loading documents, chunking text, generating embeddings, and storing vectors.

Vector search engine

Responsible for semantic retrieval using FAISS or Chroma.

Agent orchestration

Implements reasoning workflows using LangGraph.

Evaluation engine

Runs datasets of queries to measure system performance.

Experiment runner

Allows comparison of prompts, embeddings and retrieval strategies.

API service

FastAPI microservice exposing system functionality.

Frontend dashboard

Visualizes retrieval results, agent reasoning and performance metrics.

Deployment infrastructure

Docker based containerized system.

Testing the System

Every new feature must include a testing method.

Copilot must always document:

how to run the feature
how to verify output
expected system behavior

Testing methods include:

API endpoint testing with curl or Postman
unit tests using pytest
integration tests across modules
manual testing through the frontend interface

Example API test

start backend server

call query endpoint

verify response structure

confirm retrieved documents match semantic query

Performance testing should measure:

response latency
retrieval accuracy
embedding generation time

Common Pitfalls

Copilot must actively avoid the following mistakes.

jumping directly to code without understanding the system

creating duplicate logic already implemented elsewhere

breaking existing APIs

over engineering simple solutions

ignoring system performance

generating unnecessary abstractions

introducing dependencies without justification

AI assisted coding often fails due to poor architecture decisions rather than syntax errors.

Copilot must prioritize architectural integrity.

Engineering Best Practices

Copilot must follow strong software engineering principles.

write modular code

maintain clear separation of concerns

prefer composition over inheritance

keep functions small and testable

use configuration files rather than hardcoded values

document important architectural decisions

prefer simple reliable solutions

optimize only when necessary

Performance Considerations

Copilot should consider:

embedding generation latency
vector search performance
agent reasoning cost
memory usage

Solutions may include:

batch embedding generation
vector index optimization
caching frequently retrieved documents

Product Thinking

The system must also be evaluated as a product.

Copilot should consider:

who the user is
what problem is being solved
how the system provides value
how the system could scale

Every major feature should answer:

what user problem does this solve
how does this improve user workflow

Entrepreneurial Perspective

This project should train the developer to think like a builder.

Copilot should occasionally suggest:

product improvements
new features with business value
ways the system could become a SaaS product
potential customer segments

The goal is not just to build software but to create valuable solutions.

Marketing Awareness

Features should be understandable and demonstrable.

Copilot should help structure the project so it can be:

shown in a portfolio
explained to investors
demonstrated to users

Examples:

clear dashboards
visualization of AI reasoning
performance metrics

These features make the system easier to communicate.

Sales and Negotiation Mindset

Software is valuable when it solves meaningful problems.

Copilot should help articulate:

the system's unique capabilities
why it is better than simple chatbots
what makes it useful to companies

This mindset helps the developer communicate technical value effectively.

Persistent Documentation

Important documents must exist in the repository.

docs/research.md
docs/plan.md

These serve as the system's architectural memory.

Copilot must update them whenever changes occur.

Workflow Summary

All development must follow this sequence.

research the code deeply
write research findings in docs/research.md
create detailed implementation plan in docs/plan.md
refine plan through annotation cycles
generate task checklist
implement tasks
mark progress in plan.md

Code must only be written after planning approval.