pipeline {
    agent any

    tools {
        jenkins.plugins.shiningpanda.tools.PythonInstallation 'Python-3.11'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run Pytest') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                    python -m pytest tests --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Run Docker Compose') {
            steps {
                bat '''
                    docker-compose -f docker-compose.yml up -d --build
                '''
            }
        }
    }

    post {
        always {
            bat 'docker-compose -f docker-compose.yml down'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs above.'
        }
    }
}
