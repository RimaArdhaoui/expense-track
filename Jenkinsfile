pipeline {
    agent { docker { image 'python:3.12-slim' } }
    stages {
        stage('Test') {
            steps { sh 'python3 --version' }
        }
    }
}
