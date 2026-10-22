pipeline {
agent any

```
stages {
    stage('Checkout') {
        steps {
            checkout scm
        }
    }

    stage('Build Docker Image') {
        steps {
            sh 'docker build -t smart-campus-energy:v1 .'
        }
    }

    stage('Deploy to Kubernetes') {
        steps {
            sh 'kubectl apply -f deployment.yaml'
        }
    }

    stage('Verify Deployment') {
        steps {
            sh 'kubectl rollout status deployment/smart-campus-energy --timeout=120s'
        }
    }
}

post {
    success {
        echo 'Energy dashboard deployment completed successfully.'
    }

    failure {
        echo 'Deployment failed. Check the console output.'
    }
}
```

}
