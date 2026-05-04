pipeline {
    agent any

    environment {
        // NOTE: Replace 'dockerhub-credentials' with your actual Jenkins Credentials ID for Docker Hub
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials-id'
        
        // NOTE: Replace 'yourdockerhubusername' with your actual Docker Hub username
        DOCKER_IMAGE = 'nithinnkrishna/flask-app'
        
        IMAGE_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout code from the repository
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker Image: ${DOCKER_IMAGE}:${IMAGE_TAG}"
                    sh "docker build -t ${DOCKER_IMAGE}:${IMAGE_TAG} ."
                    sh "docker tag ${DOCKER_IMAGE}:${IMAGE_TAG} ${DOCKER_IMAGE}:latest"
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    echo "Pushing Docker Image to Registry..."
                    withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS_ID}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                        sh "docker push ${DOCKER_IMAGE}:${IMAGE_TAG}"
                        sh "docker push ${DOCKER_IMAGE}:latest"
                        sh "docker logout"
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            environment {
                // NOTE: Replace 'k8s-kubeconfig' with your actual Jenkins Credentials ID for Kubernetes (Secret file/Kubeconfig)
                KUBECONFIG_CREDENTIALS_ID = 'k8s-kubeconfig'
            }
            steps {
                script {
                    echo "Deploying to Kubernetes..."
                    // Replace the placeholder image in deployment.yaml with the actual built image
                    sh "sed -i 's|DOCKER_IMAGE_NAME|${DOCKER_IMAGE}:${IMAGE_TAG}|g' k8s/deployment.yaml"
                    
                    // Deploy using kubectl with the provided kubeconfig
                    withCredentials([file(credentialsId: "${KUBECONFIG_CREDENTIALS_ID}", variable: 'KUBECONFIG')]) {
                        sh "kubectl apply -f k8s/deployment.yaml"
                        sh "kubectl apply -f k8s/service.yaml"
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Clean up workspace after build
            cleanWs()
        }
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed! Please check the logs."
        }
    }
}
