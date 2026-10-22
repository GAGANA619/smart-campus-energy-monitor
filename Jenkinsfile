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
                    sh '''
                        test -f index.html
                        test -f Dockerfile
                        test -f Jenkinsfile
                        test -f deployment.yaml
                        test -f tests/test_dashboard.py
                    '''

                    echo 'All required project files are present.'
                }
            }

            stage('Run Automated Tests') {
                steps {
                    sh '''
                        mkdir -p reports
                        python3 -m unittest discover -s tests -v > reports/test-results.txt 2>&1
                        RESULT=$?
                        cat reports/test-results.txt
                        exit $RESULT
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
            sh 'docker build -t smart-campus-energy:latest .'
        }
    }

    stage('Deploy to Kubernetes') {
        when {
            expression {
                params.DEPLOY_TO_KUBERNETES
            }
        }

        steps {
            sh 'kubectl apply -f deployment.yaml'
        }
    }
}

post {
    always {
        sh '''
            mkdir -p reports
            echo "Build Number: $BUILD_NUMBER" > reports/build-info.txt
            echo "Build URL: $BUILD_URL" >> reports/build-info.txt
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
        echo 'Pipeline failed. Check the console output.'
    }
}


}
