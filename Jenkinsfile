pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps { checkout scm }
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
                    pytest -q
                '''
            }
        }
    }
}
