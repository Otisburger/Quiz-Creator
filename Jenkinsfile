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
                    "C:\\Users\\colin\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m venv venv
                    call venv\\Scripts\\activate
                    "C:\\Users\\colin\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pip install --upgrade pip
                    "C:\\Users\\colin\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pip install -r requirements.txt
                    docker-compose -f docker-compose.selenium.yml down --volumes --rmi all
                    docker-compose -f docker-compose.selenium.yml up -d --build
                    "C:\\Users\\colin\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m pytest tests --maxfail=1 --disable-warnings -q
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
            bat 'docker-compose -f docker-compose.selenium.yml down --volumes --rmi all'
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs above.'
        }
    }
}
