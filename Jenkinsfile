pipeline {
    agent any

    options {
        timestamps()
        skipDefaultCheckout(true)
    }

    parameters {
        booleanParam(
            name: 'BUILD_DOCKER_IMAGE',
            defaultValue: false,
            description: 'Build the Docker image'
        )

        booleanParam(
            name: 'DEPLOY_TO_KUBERNETES',
            defaultValue: false,
            description: 'Deploy the application to Kubernetes'
        )
    }

    stages {

        stage('Checkout Latest Code') {
            steps {
                checkout scm
                echo 'Latest repository code checked out successfully.'
            }
        }

        stage('Parallel Validation and Testing') {
            parallel {

                stage('Validate Project Files') {
                    steps {
                        bat '''
                            if not exist index.html exit /b 1
                            if not exist Dockerfile exit /b 1
                            if not exist Jenkinsfile exit /b 1
                            if not exist deployment.yaml exit /b 1
                            if not exist tests\\test_dashboard.py exit /b 1
                            echo All required project files are present.
                        '''
                    }
                }

                stage('Run Automated Tests') {
                    steps {
                        bat '''
                            if not exist reports mkdir reports
                            python -m unittest discover -s tests -v > reports\\test-results.txt 2>&1
                            set TEST_RESULT=%ERRORLEVEL%
                            type reports\\test-results.txt
                            exit /b %TEST_RESULT%
                        '''
                    }
                }
            }
        }

        stage('Build Docker Image') {
            when {
                expression {
                    params.BUILD_DOCKER_IMAGE
                }
            }

            steps {
                bat 'docker build -t smart-campus-energy:latest .'
            }
        }

        stage('Deploy to Kubernetes') {
            when {
                expression {
                    params.DEPLOY_TO_KUBERNETES
                }
            }

            steps {
                bat 'kubectl apply -f deployment.yaml'
            }
        }
    }

    post {
        always {
            bat '''
                if not exist reports mkdir reports
                echo Build Number: %BUILD_NUMBER% > reports\\build-info.txt
                echo Build URL: %BUILD_URL% >> reports\\build-info.txt
            '''

            archiveArtifacts(
                artifacts: 'reports/*.txt',
                allowEmptyArchive: true
            )
        }

        success {
            echo 'Smart Campus Energy Pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed. Check the Console Output for details.'
        }
    }
}