pipeline {
    agent any

    environment {
        SONARQUBE_ENV = 'sonarqube'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Clean') {
            steps {
                sh '''
                    rm -rf .venv __pycache__ app/__pycache__ tests/__pycache__ \
                        dist build *.egg-info gitleaks.json trivy-fs-report.json
                '''
            }
        }

        stage('Secret Scan - Gitleaks') {
            agent {
                docker { image 'zricethezav/gitleaks:latest'; args '--entrypoint=' }
            }
            steps {
                sh 'gitleaks detect --source=. --no-git --report-format=json --report-path=gitleaks.json --exit-code=1'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'gitleaks.json', allowEmptyArchive: true
                }
            }
        }

        stage('Install & Test') {
            agent {
                docker { image 'python:3.12-slim' }
            }
            steps {
                sh '''
                    python -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements.txt
                    python -m pytest -q
                '''
            }
        }

        stage('SonarQube Analysis') {
            agent {
                docker {
                    image 'sonarsource/sonar-scanner-cli:latest'
                    args '--network devsecops-net'
                }
            }
            steps {
                withSonarQubeEnv("${SONARQUBE_ENV}") {
                    sh 'sonar-scanner'
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build Artifact') {
            agent {
                docker { image 'python:3.12-slim' }
            }
            steps {
                sh '''
                    python -m venv .venv-build
                    . .venv-build/bin/activate
                    pip install --quiet build
                    python -m build
                '''
            }
        }

        stage('Publish to Nexus') {
            agent {
                docker {
                    image 'python:3.12-slim'
                    args '--network devsecops-net'
                }
            }
            environment {
                NEXUS_CREDS = credentials('nexus-creds')
            }
            steps {
                sh '''
                    python -m venv .venv-publish
                    . .venv-publish/bin/activate
                    pip install --quiet twine
                    twine upload --repository-url http://nexus:8081/repository/pypi-hosted/ \
                        -u "$NEXUS_CREDS_USR" -p "$NEXUS_CREDS_PSW" dist/*
                '''
            }
        }
        stage('Verify kind Connectivity') {
    steps {
        withCredentials([file(credentialsId: 'kubeconfig-kind', variable: 'KUBECONFIG_FILE')]) {
            sh 'kubectl --kubeconfig=$KUBECONFIG_FILE get nodes'
        }
    }
}

    }
}