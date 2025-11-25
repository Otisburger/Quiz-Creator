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
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pytest tests --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Run Docker Compose') {
            steps {
                sh '''
                    docker-compose -f docker-compose.yml up -d --build
                '''
            }
        }
    }

    post {
        always {
            sh 'docker-compose -f docker-compose.yml down'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs above.'
        }
    }
}
