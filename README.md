# AI Document Assistant

## Table of Contents
- [Introduction](#introduction)
  - [Architecture & Design Issues](#architecture--design-issues)
  - [Security Issues](#security-issues)
  - [DevOps & MLOps Issues](#devops--mlops-issues)
  - [Code Quality Issues](#code-quality-issues)
  - [Data Management Issues](#data-management-issues)
  - [Infrastructure Issues](#infrastructure-issues)
  - [Project Structure Issues](#project-structure-issues)
  - [Documentation Issues](#documentation-issues)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Usage - Running Locally](#usage---running-locally)
- [License](#license)
- [Support](#support)
- [Notes](#notes)

## Introduction
Mercury (featuring its AI assistant Hermes) is a powerful, open-source document interaction system that combines the capabilities of GPT-4 with efficient document retrieval. Built on LangChain and Chainlit, it offers a seamless web interface for both general AI assistance and intelligent document analysis.
🚀 Key Features:
- Dual-mode interface: Switch between general AI chat and document-specific interactions
- Advanced PDF processing with intelligent chunking and vector storage
- Retrieval-Augmented Generation (RAG) for accurate, context-aware responses
- Built on GPT-4 Turbo for state-of-the-art language understanding
- Clean, intuitive web interface with real-time streaming responses
Perfect for researchers, analysts, and professionals who need to quickly extract insights from documents while maintaining the flexibility of a general-purpose AI assistant. Built with Python and released under the GNU GPL v3 License.

This small project comes off the back of my newly sparked interest in large language models et al. round the beginning of 2024. As a note to myself (and to anybody who stumbles upon this repository), a lot of mistakes were made here. I decided to publish it anyway, so it can stand as a beacon of how much I've learned myself. Without further adieu, here are all the errors (big and small) I've erred in this repository. It's worth nothing that I've fixed this and made a host of new errors (undoubtedly) in RowFlows, for which the codebase is not public at this stage, but it lives at www.rowflows.com.

### Architecture & Design Issues
- Using Langchain in production (Langchain is abstraction slop) - it's unstable and changes frequently
- No clear separation of concerns between different layers (presentation, business logic, data)
- Missing proper dependency injection patterns
- No clear error handling strategy across the application

### Security Issues
- Storing secrets in JSON file instead of using environment variables or a secrets manager
- No input validation or sanitization visible in the code
- No rate limiting implementation
- Missing any kind of authentication/authorisation system
- Hardcoded configuration values that should be environment variables

### DevOps & MLOps Issues
- No CI/CD pipeline configuration
- Missing containerization (no Dockerfile)
- No monitoring or logging infrastructure
- No model versioning system
- No model performance monitoring
- Missing automated testing infrastructure (unit tests, integration tests)
- No clear deployment strategy or environment configuration

### Code Quality Issues
- Inconsistent error handling (sometimes printing, sometimes passing silently)
- Many TODOs left in code without tracking:
- Hardcoded values throughout the codebase instead of configuration
- Missing type hints in many functions
- Incomplete documentation for many functions
- No consistent logging strategy

### Data Management Issues
- No clear data validation strategy
- Missing data versioning
- No clear backup strategy for the vector store
- Inefficient document processing with potential memory issues

### Infrastructure Issues
- No scalability considerations
- Missing health checks
- No proper cleanup mechanisms for temporary files
- No proper session management

### Project Structure Issues
- Many empty __init__.py files without proper module exports
- Inconsistent project structure
- Missing proper requirements organization (dev vs prod dependencies)
- No clear API versioning strategy
- Missing proper configuration management across environments

### Documentation Issues
- Incomplete API documentation
- Missing deployment documentation
- No clear contribution guidelines
- Missing system architecture documentation
- Incomplete license headers in source files

## Getting Started
To begin your journey with, make sure Python is installed on your system. Follow these steps to set up and start engaging with your data in a whole new way:

### Installation

1. Clone the Mercury repository:
   ```bash
   git clone https:/github.com/thomasmmarshall/mercury-ai
   ```
2. Navigate to the Mercury directory:
   ```bash
   cd Mercury
   ```
3. Install the required dependencies:
   ```
   poetry install
   ```
4. Activate the environment:
   ```bash
   poetry shell
   ```

### Configuration

Create a `secrets.json` file in the `/app/` directory with your OpenAI and Azure credentials to enable the advanced NLP features:

```json
{
    "OPENAI_API_KEY": "your-openai-api-key"
}
```

### Usage - Running Locally

Run with the following command inside of the Poetry shell:

```bash
python -m chainlit run app/main.py
```

This will launch the app in your browser, where you can start your data dialogue with.

## License
This repo is available under the GNU GPL v3 License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please file an issue in the repository's issue tracker (my email).

Contact me at marshallthomasm@gmail.com

## Notes
I did not write the implementation of RAPTOR contained in this repo, this is from https://github.com/langchain-ai/langchain/blob/master/cookbook/RAPTOR.ipynb.
