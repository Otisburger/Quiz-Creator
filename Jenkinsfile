pipeline {
    agent any

    environment {
        // You can set Python version or virtualenv path here if needed
        PYTHON_ENV = "${WORKSPACE}/venv"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set up Python') {
            steps {
                sh '''
                    python3 -m venv $PYTHON_ENV
                    source $PYTHON_ENV/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Pytest') {
            steps {
                sh '''
                    source $PYTHON_ENV/bin/activate
                    pytest tests --maxfail=1 --disable-warnings -q
                '''
            }
        }

        stage('Build and Run Containers') {
            steps {
                sh '''
                    docker-compose -f docker-compose.yml build
                    docker-compose -f docker-compose.yml up -d
                '''
            }
        }

        stage('Integration Tests (Optional)') {
            steps {
                sh '''
                    source $PYTHON_ENV/bin/activate
                    pytest integration_tests --maxfail=1 --disable-warnings -q || true
                '''
            }
        }
    }

    post {
        always {
            echo 'Cleaning up containers...'
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
