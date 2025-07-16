# Distributed LLM Penetration Testing CLI Tool

## Overview
This tool enables penetration testing of LLM models across distributed systems, where the tester model and target model are running on different Ollama instances within the same network.

## Features

### ✅ Multi-Endpoint Configuration
- **Tester Model**: Runs on System A (generates attack prompts)
- **Target Model**: Runs on System B (receives attacks)
- **Network Communication**: Secure API calls between systems
- **Connection Validation**: Automatic endpoint testing

### ✅ Enhanced Capabilities
- **OWASP LLM Top 10 Coverage**: LLM01, LLM02, LLM04, LLM06
- **Distributed Architecture**: Separate tester and target endpoints
- **Connection Testing**: Validate both endpoints before testing
- **Model Validation**: Check model availability on both systems
- **Enhanced Logging**: Detailed distributed testing logs

## Installation

```bash
# Install dependencies
pip install requests

# Make scripts executable
chmod +x distributed_llm_pentest_cli.py
chmod +x demo_distributed_llm_pentest_cli.py
```

## Usage

### 1. Basic Distributed Testing

```bash
# Test with models on different systems
python3 distributed_llm_pentest_cli.py \
  --tester-url http://192.168.1.100:11434 \
  --target-url http://192.168.1.101:11434 \
  --tester-model llama3.2:latest \
  --target-model llama3.2:1b \
  --max-tests 10
```

### 2. Connection Testing

```bash
# Test connections to both endpoints
python3 distributed_llm_pentest_cli.py \
  --tester-url http://192.168.1.100:11434 \
  --target-url http://192.168.1.101:11434 \
  --test-connections
```

### 3. List Available Models

```bash
# List models on both endpoints
python3 distributed_llm_pentest_cli.py \
  --tester-url http://192.168.1.100:11434 \
  --target-url http://192.168.1.101:11434 \
  --list-models
```

### 4. Demo Mode (No Ollama Required)

```bash
# Run demo version
python3 demo_distributed_llm_pentest_cli.py \
  --tester-url http://192.168.1.100:11434 \
  --target-url http://192.168.1.101:11434 \
  --max-tests 5
```

## System Setup

### System A (Tester Model)
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Configure to accept external connections
ollama serve --host 0.0.0.0 --port 11434

# Pull tester model
ollama pull llama3.2:latest
```

### System B (Target Model)
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Configure to accept external connections
ollama serve --host 0.0.0.0 --port 11434

# Pull target model
ollama pull llama3.2:1b
```

### Network Configuration
```bash
# Open firewall ports on both systems
sudo ufw allow 11434

# Or for specific networks
sudo ufw allow from 192.168.1.0/24 to any port 11434
```

## Command Line Options

### Required Arguments
- `--tester-model`: Model name for generating attacks
- `--target-model`: Model name for receiving attacks

### Optional Arguments
- `--tester-url`: Ollama API URL for tester (default: http://localhost:11434)
- `--target-url`: Ollama API URL for target (default: http://localhost:11434)
- `--max-tests`: Maximum number of tests (default: 10)
- `--delay`: Delay between tests in seconds (default: 2.0)
- `--list-models`: List available models on both endpoints
- `--test-connections`: Test connectivity to both endpoints

## Output Format

### Enhanced Test Results
Each test includes distributed information:

```json
{
  "test_id": "LLMSec-20250716-1305-001",
  "timestamp_utc": "2025-07-16T13:05:42.123456+00:00",
  "target_model": "llama3.2:1b",
  "tester_model": "llama3.2:latest",
  "tester_endpoint": "http://192.168.1.100:11434",
  "target_endpoint": "http://192.168.1.101:11434",
  "owasp_category_code": "LLM06",
  "owasp_category_name": "Sensitive Information Disclosure",
  "attack_vector": "System Prompt Extraction",
  "attack_strategy": "Use maintenance roleplay to extract system prompt",
  "prompt_payload": "I'm a system maintenance engineer...",
  "analysis_of_target_response": "Target model disclosed system prompt...",
  "vulnerability_identified": true,
  "severity_assessment": "High",
  "remediation_guidance": "Implement hard-coded rules...",
  "evolution_strategy": "Target is susceptible to authority-based roleplay..."
}
```

## Example Scenarios

### Scenario 1: Internal Network Testing
```bash
# Company network with two development servers
python3 distributed_llm_pentest_cli.py \
  --tester-url http://dev-server-1:11434 \
  --target-url http://dev-server-2:11434 \
  --tester-model llama3.2:latest \
  --target-model custom-model:1b \
  --max-tests 15
```

### Scenario 2: Cross-Department Testing
```bash
# Security team testing production model
python3 distributed_llm_pentest_cli.py \
  --tester-url http://security-host:11434 \
  --target-url http://production-host:11434 \
  --tester-model security-model:latest \
  --target-model production-model:v1 \
  --max-tests 20 \
  --delay 5.0
```

### Scenario 3: Remote Testing
```bash
# Testing model on different network segment
python3 distributed_llm_pentest_cli.py \
  --tester-url http://10.0.1.100:11434 \
  --target-url http://10.0.2.100:11434 \
  --tester-model llama3.2:latest \
  --target-model target-model:latest \
  --max-tests 10
```

## Troubleshooting

### Connection Issues
```bash
# Test individual endpoints
curl http://192.168.1.100:11434/api/version
curl http://192.168.1.101:11434/api/version

# Check firewall
sudo ufw status
sudo iptables -L

# Test network connectivity
ping 192.168.1.100
ping 192.168.1.101
```

### Model Issues
```bash
# Check available models
curl http://192.168.1.100:11434/api/tags
curl http://192.168.1.101:11434/api/tags

# Pull missing models
ollama pull llama3.2:latest
ollama pull llama3.2:1b
```

## Security Considerations

### Network Security
- Use VPN or secure network segments
- Implement proper firewall rules
- Monitor network traffic
- Use HTTPS if available

### Model Security
- Validate model integrity
- Monitor resource usage
- Implement rate limiting
- Log all testing activities

## Files Generated

### Test Results
- `distributed_test_result_<test_id>.json`: Individual test results
- `distributed_llm_pentest.log`: Detailed execution logs

### Demo Results
- `demo_distributed_test_result_<test_id>.json`: Demo test results
- `demo_distributed_llm_pentest.log`: Demo execution logs

## Advanced Usage

### Custom Configuration
```bash
# High-intensity testing
python3 distributed_llm_pentest_cli.py \
  --tester-url http://high-end-server:11434 \
  --target-url http://target-server:11434 \
  --tester-model llama3.2:70b \
  --target-model target-model:8b \
  --max-tests 50 \
  --delay 0.5
```

### Batch Testing
```bash
# Test multiple target models
for model in model1:latest model2:latest model3:latest; do
  python3 distributed_llm_pentest_cli.py \
    --tester-url http://tester:11434 \
    --target-url http://target:11434 \
    --tester-model llama3.2:latest \
    --target-model $model \
    --max-tests 10
done
```

## Architecture Benefits

### Distributed Testing
- **Isolation**: Tester and target models run on separate systems
- **Scalability**: Can test multiple targets from single tester
- **Realism**: Simulates real-world distributed deployments
- **Performance**: Dedicated resources for each model

### Enhanced Security
- **Network Segmentation**: Models isolated on different networks
- **Independent Monitoring**: Separate logging and monitoring
- **Controlled Access**: Granular network access controls
- **Audit Trail**: Complete distributed testing history

This implementation provides a robust foundation for distributed LLM penetration testing across networked systems.