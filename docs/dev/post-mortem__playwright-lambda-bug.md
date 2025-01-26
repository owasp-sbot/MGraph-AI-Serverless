# Technical Post-Mortem: Playwright Chrome Installation in AWS Lambda

This technical analysis documents a critical performance bug encountered when running Playwright with Chrome in AWS Lambda environments. The investigation, completed in approximately 1 hour, resolved a significant cold-start performance issue where Chrome installation was taking ~1 minute on each Lambda startup. The solution reduced this to a few seconds, demonstrating how container runtime behaviors can significantly impact serverless application performance.

## Timeline and Performance Impact

- Total investigation and fix time: ~1 hour
- Main deployment pipeline time: ~4m 48s (including 1m 36s for AWS ECR publish)
- Development pipeline time: ~1m 13s
- Performance improvement: Chrome installation reduced from ~1 minute to a few seconds on Lambda cold starts

## Bug Description
During the implementation of browser automation in AWS Lambda using Playwright, we encountered a critical issue where Chrome installation would not persist in the Lambda environment despite successful local testing. This discrepancy between local and cloud environments highlighted the unique challenges of managing dependencies in serverless architectures.

## Environment Matrix
Understanding the behavior across different environments proved crucial to solving this issue. Each environment presented its own characteristics and challenges, ultimately leading to the identification of Lambda's specific runtime behavior as the root cause.

### Local Direct Environment
- OS: Host machine's operating system
- Runtime: Direct Python execution
- Chrome Installation: Works as expected
- Cache Location: User's home directory
- Persistence: Full persistence between runs

### Local Docker Environment
- OS: Container Linux environment
- Runtime: Docker container
- Chrome Installation: Successfully installed during build
- Cache Location: `/root/.cache/ms-playwright/`
- Persistence: Maintained between container restarts

### AWS Lambda Docker Environment
- OS: AWS Lambda Linux environment
- Runtime: Lambda container runtime
- Chrome Installation: Installed during build but not accessible at runtime
- Cache Location: `/root/.cache/ms-playwright/` (empty at runtime)
- Persistence: Cache directory overwritten by Lambda's ephemeral storage

## Investigation Process
The investigation followed a systematic approach to identify why Chrome installation worked perfectly in local environments but failed in AWS Lambda. This process involved testing across multiple environments and developing hypotheses about potential causes.

### Initial Hypothesis
1. Chrome installation failing during build
2. Permissions issues in Lambda environment
3. Path configuration differences between environments

### Environment Tests
Local Docker test revealed proper installation:
```python
def test_2_playwright__check_docker_install_location(self):
    assert self.shell.ls('/root/.cache/ms-playwright/chromium-1148/chrome-linux/chrome') == '/root/.cache/ms-playwright/chromium-1148/chrome-linux/chrome\n'
    # Full installation verified
```

AWS Lambda test showed missing files:
```python
def test_2_playwright__check_docker_install_location(self):
    assert self.shell.ls('/root/.cache/ms-playwright/chromium-1148/chrome-linux/chrome') == ''
    # Empty installation directory
```

## Root Cause Analysis
Through careful investigation and testing, we identified that AWS Lambda's unique container runtime behavior was the source of our issues. This finding led to a deeper understanding of how Lambda handles ephemeral storage and its impact on application dependencies.

The issue stems from AWS Lambda's container runtime behavior:
1. Docker build installs Chrome to `/root/.cache`
2. Lambda runtime mounts ephemeral storage at `/root/.cache`
3. Original installation becomes inaccessible
4. Specific to Lambda environment due to its ephemeral storage architecture

## Solution
After identifying the root cause, we developed a solution that would work consistently across all environments while respecting Lambda's runtime constraints. The key was to use a persistent storage location that wouldn't be affected by Lambda's ephemeral storage mechanism.

### Implementation Changes
1. Modified Dockerfile for persistent installation:
```dockerfile
RUN PLAYWRIGHT_BROWSERS_PATH=/opt/playwright playwright install --with-deps chromium
```

2. Updated application Chrome path:
```python
LINUX__PLAYWRIGHT__CHROME__PATH = '/opt/playwright/chromium-1148/chrome-linux/chrome'
```

### Why This Works
- `/opt` directory persists in Lambda environment
- Consistent path across all environments
- Dependencies remain accessible during Lambda execution

## Lambda Shell: Innovative Debugging Solution
Debugging issues in containerized environments, especially in serverless functions like AWS Lambda, presents unique challenges. Traditional debugging approaches often fall short due to the isolated nature of these environments. This section describes an innovative solution we developed to address these limitations.

### The Challenge
Traditional debugging in Lambda environments is difficult due to:
1. No direct code execution in containers
2. Long deployment cycles for code changes
3. Limited logging capabilities
4. Environment-specific behaviors

### Lambda Shell Implementation
Taking inspiration from security testing methodologies, we developed a controlled remote code execution capability that transforms debugging containerized applications. This approach provides unprecedented visibility into runtime environments while maintaining security controls.

### How It Works
1. Local test initiates debug session
2. Function code transmitted as text to FastAPI endpoint
3. Server-side execution via controlled Python eval
4. Results captured and returned to local environment
5. Real-time feedback loop established

### Security Considerations
- Feature requires explicit enablement
- Special authentication required
- Controlled execution environment
- Limited to development/debugging contexts

### Benefits
1. Rapid iteration on environment-specific issues
2. Direct verification of file systems and paths
3. Real-time testing of hypotheses
4. Significant reduction in debug cycle time

### Example Usage
```python
def debug_chrome_installation():
    # Function definition sent to Lambda
    result = check_installation_paths()
    return result

# Local execution
response = self.shell.function(debug_chrome_installation)
```

## Lessons Learned
This investigation provided valuable insights into container runtime behaviors and the importance of understanding environment-specific characteristics when deploying applications to serverless platforms. The experience also demonstrated the value of innovative debugging approaches in modern cloud architectures.

1. AWS Lambda container runtime overrides certain directories
2. Critical runtime dependencies need persistent locations
3. Environment variables can ensure correct installation paths
4. Advanced debugging capabilities crucial for container environments
5. Environment-specific testing essential for Lambda deployments
