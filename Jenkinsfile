pipeline {
  agent any

  environment {
    registryCredential = 'dockerhublogin'
  }

  stages {
    stage('Checkout') {
      steps {
        git 'https://github.com/Otisburger/Quiz-Creator.git'
      }
    }

    stage('Build Images') {
      steps {
        script {
            docker.build('cotoole2/react-frontend:latest', 'frontend/')
            docker.build('cotoole2/flask-backend:latest', '.')
        }
      }
    }

    stage('Push Images') {
      steps {
        script {
          docker.withRegistry("https://index.docker.io/v1/", 'dockerhub-creds'){
            docker.image("cotoole2/react-frontend:latest").push()
            docker.image("cotoole2/flask-backend:latest").push()
          }
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        script {
            withCredentials([file(credentialsId: 'minikube-kubeconfig', variable: 'KUBECONFIG')]) {
                bat 'kubectl get pods --namespace=default'
                bat 'kubectl apply -f frontend-deployment.yaml'
                bat 'kubectl apply -f backend-deployment.yaml'
                bat 'kubectl set image deployment/frontend frontend=cotoole2/react-frontend:latest --namespace=default'
                bat 'kubectl set image deployment/backend backend=cotoole2/flask-backend:latest --namespace=default'
            }
        }
      }
    }
  }

  post {
    success {
      echo "✅ Deployed frontend and backend version latest to Kubernetes"
    }
    failure {
      echo "❌ Deployment failed. Check logs above."
    }
  }
}