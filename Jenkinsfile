pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run Pytest') {
            steps {
                bat '''
                    py -m venv venv
                    call venv\\Scripts\\activate
                    py -m pip install --upgrade pip
                    py -m pip install -r requirements.txt
                    py -m pytest tests --maxfail=1 --disable-warnings -q
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
