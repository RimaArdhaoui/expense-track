pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
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

        stage('Secret Scan - Gitleaks') {
            agent {
                docker { image 'zricethezav/gitleaks:latest'; args '--entrypoint=' }
            }
            steps {
                sh 'gitleaks detect --source=. --no-git --report-format=json --report-path=gitleaks.json --exit-code=1'
            }
        }
    }
}