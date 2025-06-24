# LLM-based SQL and Statistics Generation

This project leverages LLMs to generate SQL based on UnifiedServer database schema, perform data retrieval, and create and run Python scripts for data analysis. The system is designed for rapid prototyping, data exploration, and automated script generation.

## Setup
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <directory>
   ```

2. **Build and run with Docker**:
   ```bash
   docker build -t datagenie .
   docker run -p 8000:8000 datagenie
   ```

3. **Add MCP to LLM tool list**:
   ```json
   {
      "datagenie": {
         "type": "http",
         "url": "http://localhost:8000/mcp/"
      }
   }
   ```
   For GitHub Copilot:
   ```
   CTRL+SHIFT+P -> MCP: Add Server -> HTTP -> http://localhost:8000/mcp/
   ```

## Testing

### Run Tests
- To run all tests:
  ```bash
  uv run pytest
  ```

### Unit Tests
- Pytest validate individual components of the system.

### Integration Tests
- Integration tests build a Docker image based on the current directory, run a container, and perform tests against the running container.

## Contribution
1. **Create a separate branch**:
   ```bash
   git checkout -b <branch-name>
   ```
2. **Commit changes**:
   ```bash
   git commit -m "<commit-message>"
   ```
3. **Create a pull request**:
   Submit your branch for review.

4. **Code Formatting**:
   Run the following command to format your code:
   ```bash
   uv run black .
   ```

