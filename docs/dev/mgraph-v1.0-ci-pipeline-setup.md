# MGraph v1.0.0 CI/CD Pipeline Setup

*Tech guide to the CI/CD configuration of the MGraph-AI-Serverless repository which leverages the OSBot packages*

## Why This Matters
Setting up proper infrastructure before writing application code is crucial for long-term project success. Each component in this guide addresses specific challenges that become exponentially harder to implement as the codebase grows. By establishing these foundations early, we create a robust development environment that supports quality, testing, and automated deployments from day one.

This guide specifically showcases the implementation in the [MGraph-AI-Serverless](https://github.com/owasp-sbot/MGraph-AI-Serverless) repository, leveraging the power of several open-source packages:
- OSBot-Util: Core utilities and helpers
- OSBot-AWS: AWS integration and deployment tools
- OSBot-Fast-API: FastAPI extensions and utilities

### Key Benefits
- Consistent development environment across team members
- Automated quality checks and deployments from the start
- Clear separation of development and production environments
- Built-in testing practices that scale with code
- Infrastructure-as-code approach for reproducible deployments
- Leveraging battle-tested OSBot packages for rapid development

## The CI/CI pipeline for v1.0.0
On the topic of good engineering and quality code, here is the recommended CI/CD pipeline to create on a repo before adding application code. 

This v1.0.0 approach ensures quality, maintainability, and proper CI/CD from day one.

Here are all the steps executed in this first version: 

- 1️⃣ Git repo 
- 2️⃣ FastAPI base app 
- 3️⃣ CI pipeline (dev and main) 
- 4️⃣ Unit, integration and QA tests 
- 5️⃣ 100% code coverage 
- 6️⃣ Auto-tagging on commits 
- 7️⃣ Create Docker container 
- 8️⃣ Push Docker container to AWS ECR 
- 9️⃣ Create AWS Lambda 
- 1️⃣0️⃣ Enable AWS Function URL 
- 1️⃣0️⃣ Ensure AWS Lambda/FastAPI works

## 1. Repository Setup
Repository setup establishes the foundation for the entire development workflow. A well-structured repository ensures consistent development practices, clear code organization, and efficient collaboration. The directory structure follows separation of concerns principles and supports independent testing of each component. The MGraph-AI-Serverless repository leverages OSBot packages for enhanced functionality, type safety, and AWS integration, making it essential to establish proper dependency management from the start.

### Initial Structure
Sets up the foundational directory structure required for proper separation of concerns. This layout supports independent development, testing, and deployment processes while maintaining clear organization of application components.

```bash
mkdir my-fastapi-project
cd my-fastapi-project
git init

# Create core directories
mkdir -p {src,tests/{unit,integration,qa},deploy/{docker,lambdas},.github/workflows}

# Create essential files
touch README.md LICENSE pyproject.toml requirements-test.txt
touch .gitignore .env.example
```

### Base Configuration Files
Configuration files establish project dependencies, testing requirements, and build settings. Poetry provides reliable dependency management while maintaining reproducible environments.

**pyproject.toml**
```toml
[tool.poetry]
name        = "my_fastapi_project"
version     = "v0.0.1"
description = "FastAPI Serverless Project"
authors     = ["An Name <an.email@domain.com>"]
license     = "Apache 2.0"
readme      = "README.md"

[tool.poetry.dependencies]
python           = "^3.11"
fastapi          = "*"
mangum           = "*"
httpx           = "*"
uvicorn         = "*"
osbot-util      = "*"
osbot-aws       = "*"
osbot-fast-api  = "*"

[build-system]
requires      = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

## 2. FastAPI Base Application
The application leverages OSBot packages for enhanced FastAPI functionality, clean route management, and type-safe operations.

### Core Application Structure
Organizes the application following a modular architecture that separates routes, utilities, and core application logic. This structure facilitates maintainability, testing, and future expansion while leveraging OSBot packages for enhanced functionality.

```
src/
├── fast_api/
│   ├── MGraph_AI_Serverless__Fast_API.py
│   └── routes/
│       └── Routes__Info.py
├── utils/
│   └── Version.py
└── handler.py
```

### Main FastAPI Application (MGraph_AI_Serverless__Fast_API.py)
The main application class extends OSBot's Fast_API base class to provide enhanced routing capabilities and CORS support. This class serves as the core FastAPI application configuration, managing route registration and API settings.
```python
from osbot_fast_api.api.Fast_API                       import Fast_API
from mgraph_ai_serverless.fast_api.routes.Routes__Info import Routes__Info

class MGraph_AI_Serverless__Fast_API(Fast_API):
    base_path  : str  = '/'
    enable_cors: bool = True

    def setup_routes(self):
        self.add_routes(Routes__Info)
```

### Info Routes (Routes__Info.py)
Implements basic API information endpoints using OSBot's route management system. This module provides version and health check endpoints, demonstrating the clean route organization possible with OSBot-Fast-API.
```python
from osbot_fast_api.api.Fast_API_Routes import Fast_API_Routes
from mgraph_ai_serverless.utils.Version import version__mgraph_ai_serverless

ROUTES_PATHS__INFO = ['/info/version', '/info/ping']

class Routes__Info(Fast_API_Routes):
    tag: str = 'info'

    def ping(self):
        return 'pong'

    def version(self):
        return {'version': version__mgraph_ai_serverless}
    
    def setup_routes(self):
        self.add_route_get(self.ping)
        self.add_route_get(self.version)
```

### Version Management (Version.py)
Handles version management using OSBot's Type-Safe utilities. This class provides robust version file handling and ensures type safety throughout version operations. It demonstrates OSBot-Utils' file handling and type safety capabilities.
```python
import mgraph_ai_serverless
from osbot_utils.type_safe.Type_Safe import Type_Safe
from osbot_utils.utils.Files         import file_contents, path_combine

class Version(Type_Safe):
    FILE_NAME_VERSION = 'version'

    def path_code_root(self):
        return mgraph_ai_serverless.path

    def path_version_file(self):
        return path_combine(self.path_code_root(), self.FILE_NAME_VERSION)

    def value(self):
        value = file_contents(self.path_version_file()) or ""
        return value.strip()

version__mgraph_ai_serverless = Version().value()
```

### AWS Lambda Handler (handler.py)
Configures the AWS Lambda integration using Mangum. This module sets up the FastAPI application for both local development and AWS Lambda deployment, leveraging OSBot's environment management utilities.
```python
from mangum                                                       import Mangum
from osbot_utils.utils.Env                                        import get_env
from mgraph_ai_serverless.fast_api.MGraph_AI_Serverless__Fast_API import MGraph_AI_Serverless__Fast_API

fast_api__mgraph_ai_serverless = MGraph_AI_Serverless__Fast_API().setup()
app                            = fast_api__mgraph_ai_serverless.app()
run                            = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    port = get_env('PORT', 8080)
    uvicorn.run(app, host="0.0.0.0", port=port)
```

### Test Objects Setup
Centralizes test object creation for consistent testing across the application. This module provides pre-configured FastAPI instances and test clients, ensuring uniform test conditions throughout the test suite.
```python
from mgraph_ai_serverless.fast_api.MGraph_AI_Serverless__Fast_API import MGraph_AI_Serverless__Fast_API

mgraph_ai_serverless__fast_api         = MGraph_AI_Serverless__Fast_API().setup()
mgraph_ai_serverless__fast_api__app    = mgraph_ai_serverless__fast_api.app()
mgraph_ai_serverless__fast_api__client = mgraph_ai_serverless__fast_api.client()
```

## 3. Docker Configuration
The Docker setup provides a consistent environment for both local development and AWS Lambda deployment, leveraging the AWS Lambda Adapter for seamless serverless execution. Our configuration incorporates OSBot packages and necessary system dependencies, ensuring compatibility across development and production environments. The multi-stage build process optimizes container size while maintaining full functionality and development capabilities.

### Dockerfile
Multi-stage Dockerfile that creates a production-ready container with all necessary dependencies. It includes system packages, Python dependencies, and the AWS Lambda adapter, optimized for both local development and serverless deployment.
```dockerfile
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install mangum uvicorn httpx fastapi python-multipart
RUN pip install osbot-aws osbot-fast-api

COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.4 /lambda-adapter /opt/extensions/lambda-adapter

RUN python --version
ENV PORT=8080

WORKDIR /app
COPY ../../../mgraph_ai_serverless /app/mgraph_ai_serverless

ENV PYTHONPATH="/app"

COPY ./deploy/docker/mgraph-ai-serverless/start.sh /app/start.sh

CMD ["./start.sh"]
```

### docker-compose.yml
Defines the local development environment configuration. This file specifies build context, platform requirements, and port mappings for consistent local testing and development.
```yaml
services:
  mgraph_ai_serverless:
    build:
      context: ../../..
      dockerfile: ./deploy/docker/mgraph-ai-serverless/Dockerfile
    platform: linux/amd64
    container_name: mgraph_ai_serverless
    tty: true
    ports:
      - "8080:8080"
```

### start.sh
Container entry point script that launches the FastAPI application using Uvicorn. This script ensures proper server configuration for both local development and production environments.
```bash
#!/bin/bash
uvicorn mgraph_ai_serverless.lambdas.handler:app --host 0.0.0.0 --port 8080
```

### Lambda Deployment Script
Implements AWS Lambda deployment using OSBot-AWS utilities. This script handles credential management, Lambda function configuration, and deployment automation, showcasing OSBot-AWS's deployment capabilities.
```python
from mgraph_ai_serverless.utils.Version import version__mgraph_ai_serverless
from osbot_utils.type_safe.Type_Safe    import Type_Safe
from osbot_utils.utils.Env              import get_env, load_dotenv
from osbot_aws.AWS_Config               import aws_config
from osbot_aws.deploy.Deploy_Lambda     import Deploy_Lambda

class Deploy_Lambda__MGraph_AI_Serverless(Type_Safe):
    lambda_name: str = 'mgraph_ai_serverless'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_aws_credentials()
        self.deploy_lambda   = Deploy_Lambda(self.lambda_name)
        self.lambda_function = self.deploy_lambda.lambda_function()

    def deploy(self):
        self.lambda_setup            ()
        self.deploy_lambda.deploy    ()
        self.lambda_setup_post_update()

    def invoke(self):
        with self.lambda_function as _:
            result = _.invoke()
            return result

    def lambda_setup(self):
        self.deploy_lambda.set_container_image(self.ecr_image_uri())
        env_variables = {}
        self.deploy_lambda.set_env_variables(env_variables)

    def lambda_setup_post_update(self):
        with self.lambda_function as _:
            if _.function_url_exists() is False:
                _.function_url_create_with_public_access()

    def ecr_image_uri(self):
        account_id  = aws_config.account_id ()
        region_name = aws_config.region_name()
        image_name  = self.lambda_name
        image_tag   = version__mgraph_ai_serverless
        return f'{account_id}.dkr.ecr.{region_name}.amazonaws.com/{image_name}:{image_tag}'

    def setup_aws_credentials(self):
        load_dotenv()
        aws_config.set_aws_session_account_id(get_env('AWS_ACCOUNT_ID'))
        aws_config.set_region                (get_env('AWS_DEFAULT_REGION'))
        aws_config.set_aws_access_key_id     (get_env('AWS_ACCESS_KEY_ID'))
        aws_config.set_aws_secret_access_key (get_env('AWS_SECRET_ACCESS_KEY'))
```

### Lambda Deployment Tests
```python
from unittest                                           import TestCase
from mgraph_ai_serverless.utils.Version                 import version__mgraph_ai_serverless
from deploy.lambdas.Deploy_Lambda__MGraph_AI_Serverless import Deploy_Lambda__MGraph_AI_Serverless

class test_Deploy_Lambda__MGraph_AI_Serverless(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.deploy_lambda = Deploy_Lambda__MGraph_AI_Serverless()

    def test_deploy_lambda(self):
        with self.deploy_lambda as _:
            result = _.lambda_deploy()
            assert result == {'body': 'Hello from Docker Lambda!', 'statusCode': 200}

    def test_ecr_image_uri(self):
        with self.deploy_lambda as _:
            ecr_image_uri = _.ecr_image_uri()
            assert ecr_image_uri == f'{*****}.dkr.ecr.eu-west-1.amazonaws.com/{*****}:{version__mgraph_ai_serverless}'
```

## 4. Testing Framework
The testing framework demonstrates comprehensive test coverage across multiple layers using OSBot packages for enhanced capabilities. 

The testing strategy encompasses unit tests for core functionality, integration tests for API endpoints, HTTP tests using OSBot Fast_API_Server, client tests for API consumption, QA tests for deployed Lambda functions, and live Lambda integration tests. 

This multi-layered approach ensures robust validation of all system components and their interactions.

### Unit Tests
Core unit tests ensuring the reliability of fundamental components. These tests verify version management, route configuration, and basic functionality using Python's unittest framework and OSBot's testing utilities.

**test_Version.py**
```python
import mgraph_ai_serverless
from unittest                           import TestCase
from osbot_utils.utils.Files            import parent_folder, file_name
from mgraph_ai_serverless.utils.Version import Version, version__mgraph_ai_serverless

class test_Version(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.version = Version()

    def test_path_code_root(self):
        assert self.version.path_code_root() == mgraph_ai_serverless.path

    def test_path_version_file(self):
        with self.version as _:
            assert parent_folder(_.path_version_file()) == mgraph_ai_serverless.path
            assert file_name(_.path_version_file())     == 'version'

    def test_value(self):
        assert self.version.value() == version__mgraph_ai_serverless
```

**test_Routes__Info.py**
```python
from unittest                                           import TestCase
from mgraph_ai_serverless.fast_api.routes.Routes__Info  import Routes__Info
from mgraph_ai_serverless.utils.Version                 import version__mgraph_ai_serverless

class test_Routes__Info(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.routes_info = Routes__Info()

    def test_version(self):
        assert self.routes_info.version() == {'version': version__mgraph_ai_serverless}

    def test_setup_routes(self):
        with self.routes_info as _:
            assert _.routes_paths() == []
            _.setup_routes()
            assert _.routes_paths() == ['/ping', '/version']
```

### Integration Tests
Validates component interactions and API behavior. These tests use FastAPI's TestClient to verify endpoint functionality, OpenAPI documentation, and route configuration.
**test__int__handler.py**
```python
from unittest                             import TestCase
from starlette.testclient                 import TestClient
from mgraph_ai_serverless.lambdas.handler import app

class test__int__handler(TestCase):
    @classmethod
    def setUp(cls):
        cls.client = TestClient(app)

    def test_openapi(self):
        response = self.client.get("/openapi.json")
        assert response.status_code == 200
        assert response.json().get("openapi") == "3.1.0"
```

**test__int__Routes__Info.py**
```python
from unittest                                          import TestCase
from mgraph_ai_serverless.fast_api.routes.Routes__Info import Routes__Info
from mgraph_ai_serverless.utils.Version                import version__mgraph_ai_serverless

class test__int__Routes__Info(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.routes_mgraph_ai_serverless = Routes__Info()

    def test_routes_setup(self):
        with self.routes_mgraph_ai_serverless as _:
            assert _.tag == 'info'
            _.setup_routes()
            assert '/version' in _.routes_paths()

    def test__version(self):
        with self.routes_mgraph_ai_serverless as _:
            assert _.version() == {'version': version__mgraph_ai_serverless}
```

### HTTP Tests
Tests the API through real HTTP requests using OSBot's Fast_API_Server. These tests validate the complete request-response cycle in a production-like environment.
**test__http__Routes__Info.py**
```python
from unittest                                                           import TestCase
from osbot_fast_api.utils.Fast_API_Server                               import Fast_API_Server
from mgraph_ai_serverless.testing.mgraph_ai_serverless__objs_for_tests import mgraph_ai_serverless__fast_api__app
from mgraph_ai_serverless.utils.Version                                import version__mgraph_ai_serverless

class test__http__Routes__Info(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fast_api_server = Fast_API_Server(app=mgraph_ai_serverless__fast_api__app)
        cls.fast_api_server.start()
        assert cls.fast_api_server.is_port_open() is True

    @classmethod
    def tearDownClass(cls):
        cls.fast_api_server.stop()
        assert cls.fast_api_server.is_port_open() is False

    def test_http__uk__articles_html(self):
        response = self.fast_api_server.requests_get('/info/version')
        assert response.status_code == 200
        assert response.json()      == {'version': version__mgraph_ai_serverless}
```

### Client Tests
Verifies API behavior from a client perspective using pre-configured test clients. These tests ensure the API meets consumer expectations and maintains consistent responses.
**test__client__Routes__Info.py**
```python
from unittest                                                           import TestCase
from mgraph_ai_serverless.testing.mgraph_ai_serverless__objs_for_tests  import mgraph_ai_serverless__fast_api__client
from mgraph_ai_serverless.utils.Version                                 import version__mgraph_ai_serverless

class test__client__Routes__Info(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = mgraph_ai_serverless__fast_api__client

    def test_raw__uk__homepage(self):
        response = self.client.get('/info/version')
        assert response.status_code == 200
        assert response.json()      == {'version': version__mgraph_ai_serverless}
```

### QA Tests
End-to-end tests against the deployed Lambda function. These tests validate the complete system in the production environment, ensuring proper AWS integration and API functionality.
**test__qa__Routes__Info.py**
```python
import pytest
import requests
from unittest                                           import TestCase
from deploy.lambdas.Deploy_Lambda__MGraph_AI_Serverless import Deploy_Lambda__MGraph_AI_Serverless
from osbot_utils.utils.Env                              import not_in_github_action
from mgraph_ai_serverless.utils.Version                 import version__mgraph_ai_serverless

class test__qa__Routes__Info(TestCase):
    @classmethod
    def setUpClass(cls):        
        cls.deploy_lambda   = Deploy_Lambda__MGraph_AI_Serverless()
        cls.lambda_function = cls.deploy_lambda.lambda_function
        cls.lambda_url      = cls.lambda_function.function_url()
        cls.session         = requests.Session()

    def requests_get(self, endpoint, params=None):
        response = self.session.get(f"{self.lambda_url}/{endpoint}", params=params)
        response.raise_for_status()
        return response

    def test_raw_html_live(self):
        if not_in_github_action():
            pytest.skip("This test can only be executed in GH Actions after the deployment of the latest lambda")
        response = self.requests_get('info/version')
        assert response.status_code == 200
        assert response.json() == {'version': version__mgraph_ai_serverless}
```

### Lambda Integration Tests
Comprehensive tests for AWS Lambda deployment and execution. These tests verify Lambda configuration, function URLs, and proper handling of AWS Lambda events using OSBot-AWS utilities.
**test__live_lambda_function.py**
```python
from unittest                                           import TestCase
from deploy.lambdas.Deploy_Lambda__MGraph_AI_Serverless import Deploy_Lambda__MGraph_AI_Serverless
from osbot_utils.utils.Objects                          import dict_to_obj, __

class test__live_lambda_function(TestCase):
    @classmethod
    def setUpClass(cls):        
        cls.deploy_lambda   = Deploy_Lambda__MGraph_AI_Serverless()
        cls.lambda_function = cls.deploy_lambda.lambda_function

    def test__check_lambda_deployment(self):
        with self.lambda_function as _:
            assert _.exists()              is True
            assert _.function_url_exists() is True

    def lambda_payload(self, path='/', method='GET', headers=None):
        return {
            "headers"       : headers or {},
            "rawPath"       : path,
            "requestContext": {"http": {"method": method}}
        }

    def test_invoke(self):
        with self.lambda_function as _:
            assert obj(_.invoke()) == __(detail='Not Found')            

obj = dict_to_obj
```

## 5. CI Pipeline Setup
Continuous Integration ensures code quality and automated deployments. This implementation leverages OSBot GitHub Actions for standardized, reusable workflows that handle everything from testing to AWS Lambda deployment. The pipeline incorporates automatic version management, PyPI package publishing, Docker image creation and deployment to AWS ECR, Lambda function updates, and post-deployment validation through QA tests. This comprehensive automation ensures reliable and consistent deployments while maintaining high code quality standards.

### GitHub Actions Workflows


**.github/workflows/ci-pipeline-dev.yml**

Development pipeline configuration that handles testing, version management, and package publishing. This workflow ensures code quality and proper versioning for development builds.

```yaml
name: CI Pipeline - DEV
on:
  workflow_dispatch:
  push:
    branches:
      - dev

env:
  GIT__BRANCH      : 'dev'
  RELEASE_TYPE     : 'minor'
  PACKAGE_NAME     : 'mgraph_ai_serverless'

jobs:
  run-tests:
    name: "Run tests"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: "run-tests"
        uses: ./.github/actions/run-tests

  increment-tag:
    name: Increment Tag - DEV
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Increment Tag
        uses: owasp-sbot/OSBot-GitHub-Actions/.github/actions/git__increment-tag@dev
        with:
          release_type: ${{ env.RELEASE_TYPE }}
    needs:
      - run-tests

  publish-to-pypi:
    name: "Publish to: PYPI"
    permissions:
      id-token: write
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Git Update Current Branch
        uses: owasp-sbot/OSBot-GitHub-Actions/.github/actions/git__update_branch@dev
      - name: publish-to-pypi
        uses: owasp-sbot/OSBot-GitHub-Actions/.github/actions/pypi__publish@dev
    needs:
      - increment-tag
```

**.github/workflows/ci-pipeline-main.yml**

Production deployment pipeline that extends the development workflow with additional steps for AWS ECR publishing, Lambda deployment, and post-deployment validation. This workflow ensures reliable production deployments with comprehensive testing.

```yaml
name: CI Pipeline - Main
on:
  workflow_dispatch:
  push:
    branches:
      - main

env:
  GIT__BRANCH      : 'main'
  RELEASE_TYPE     : 'major'
  PACKAGE_NAME     : 'mgraph_ai_serverless'
  DOCKER__CONTEXT  : "."
  DOCKER__FILE     : './deploy/docker/mgraph-ai-serverless/Dockerfile'

jobs:
  run-tests:
    name: "Run tests"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: "run-tests"
        uses: ./.github/actions/run-tests
        env:
          AWS_ACCOUNT_ID       : ${{ secrets.AWS_ACCOUNT_ID__************** }}
          AWS_ACCESS_KEY_ID    : ${{ secrets.AWS_ACCESS_KEY_ID__************** }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY__************** }}
          AWS_DEFAULT_REGION   : ${{ secrets.AWS_DEFAULT_REGION__************** }}

  increment-tag:
    name: Increment Tag - Main
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Increment Tag
        uses: owasp-sbot/OSBot-GitHub-Actions/.github/actions/git__increment-tag@dev
        with:
          release_type: ${{ env.RELEASE_TYPE }}
    needs:
      - run-tests

  publish-to-pypi:
    name: "Publish to: PYPI"
    permissions:
      id-token: write
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Git Update Current Branch
        uses: owasp-sbot/OSBot-GitHub-Actions/.github/actions/git__update_branch@dev
      - name: publish-to-pypi
        uses: owasp-sbot/OSBot-GitHub-Actions/.github/actions/pypi__publish@dev
    needs:
      - increment-tag

  publish-to-aws-ecr:
    name: "Publish to: AWS ECR"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: "Wait for PyPI publish"
        uses: owasp-sbot/OSBot-GitHub-Actions/.github/actions/pypi__wait-for-publish@dev
      - name: "Publish to: AWS ECR"
        uses: owasp-sbot/OSBot-GitHub-Actions/.github/actions/aws__publish__ecr@dev
        env:
          AWS_ACCOUNT_ID       : ${{ secrets.AWS_ACCOUNT_ID__************** }}
          AWS_ACCESS_KEY_ID    : ${{ secrets.AWS_ACCESS_KEY_ID__************** }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY__************** }}
          AWS_DEFAULT_REGION   : ${{ secrets.AWS_DEFAULT_REGION__************** }}
    needs:
      - publish-to-pypi

  deploy-lambda-function:
    name: Deploy Lambda Function
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Tests and Integration Tests
        uses: ./.github/actions/aws__deploy-lambda
        env:
          AWS_ACCOUNT_ID        : ${{ secrets.AWS_ACCOUNT_ID__************** }}
          AWS_ACCESS_KEY_ID     : ${{ secrets.AWS_ACCESS_KEY_ID__************** }}
          AWS_SECRET_ACCESS_KEY : ${{ secrets.AWS_SECRET_ACCESS_KEY__************** }}
          AWS_DEFAULT_REGION    : ${{ secrets.AWS_DEFAULT_REGION__************** }}
    needs:
      - publish-to-aws-ecr

  run-qa-tests:
    name: "Run QA Tests"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Tests and Integration Tests
        uses: ./.github/actions/aws__run-qa-tests
        env:
          AWS_ACCOUNT_ID        : ${{ secrets.AWS_ACCOUNT_ID__************** }}
          AWS_ACCESS_KEY_ID     : ${{ secrets.AWS_ACCESS_KEY_ID__************** }}
          AWS_SECRET_ACCESS_KEY : ${{ secrets.AWS_SECRET_ACCESS_KEY__************** }}
          AWS_DEFAULT_REGION    : ${{ secrets.AWS_DEFAULT_REGION__************** }}
    needs:
      - deploy-lambda-function
```

### Lambda Deployment Action

**.github/actions/aws__deploy-lambda/action.yml**

Reusable GitHub Action that handles AWS Lambda deployment, including dependency management and configuration updates. This action leverages OSBot-AWS for streamlined Lambda deployments and integrates with the main CI/CD pipeline.


```yaml
name: "aws__deploy-lambda"
description: "aws__deploy_lambda"

runs:
  using: "composite"
  steps:
    - uses: actions/checkout@v4
    
    - name: Poetry - Install Dependencies
      uses: owasp-sbot/OSBot-GitHub-Actions/.github/actions/poetry__install@dev
    
    - name: Git Update Current Branch
      uses: owasp-sbot/OSBot-GitHub-Actions/.github/actions/git__update_branch@dev
    
    - name: deploy lambda
      shell: bash
      run: |
        echo "Deploying lambda function"        
        poetry run python ./deploy/lambdas/Deploy_Lambda__MGraph_AI_Serverless.py
```