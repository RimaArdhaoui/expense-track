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

        stage('Filesystem Scan - Trivy') {
            agent {
                docker { image 'aquasec/trivy:latest'; args '--entrypoint=' }
            }
            steps {
                sh '''
                    trivy fs --severity HIGH,CRITICAL --exit-code 1 \
                        --format json -o trivy-fs-report.json .
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy-fs-report.json', allowEmptyArchive: true
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
    }
}