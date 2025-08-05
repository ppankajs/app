pipeline {
  agent any

  environment {
    IMAGE_NAME = "self-healing-app"
    DOCKER_REGISTRY = "your-dockerhub-username"
    TAG = "v${BUILD_NUMBER}"
  }

  stages {

    stage('Clone Repo') {
      steps {
        git 'https://github.com/yourusername/self_healing_flask_pipeline_bundle.git'
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          docker.build("${DOCKER_REGISTRY}/${IMAGE_NAME}:${TAG}")
        }
      }
    }

    stage('Push Docker Image') {
      steps {
        script {
          docker.withRegistry('', 'dockerhub-credentials-id') {
            docker.image("${DOCKER_REGISTRY}/${IMAGE_NAME}:${TAG}").push()
          }
        }
      }
    }

    stage('Deploy PostgreSQL') {
      steps {
        sh 'kubectl apply -f k8s/postgres.yaml'
      }
    }

    stage('Deploy Flask App') {
      steps {
        // Replace image tag in deployment file before applying
        sh """
          sed 's|your-dockerhub-username/self-healing-app:latest|${DOCKER_REGISTRY}/${IMAGE_NAME}:${TAG}|' k8s/app-deployment.yaml | kubectl apply -f -
        """
      }
    }

    stage('Deploy CronJobs (Self-Healing)') {
      steps {
        script {
          def cronJobs = [
            "cron-failure-classification.yaml",
            "cron-trust-score.yaml",
            "cron-health-scoring.yaml",
            "cron-rollback.yaml"
          ]

          for (cron in cronJobs) {
            sh """
              sed 's|your-image-name|${DOCKER_REGISTRY}/${IMAGE_NAME}:${TAG}|' k8s/cronjobs/${cron} | kubectl apply -f -
            """
          }
        }
      }
    }

    stage('OPA: Apply Constraint Templates') {
      steps {
        sh '''
          kubectl apply -f opa/templates/label-template.yaml
          kubectl apply -f opa/templates/probes-template.yaml
        '''
      }
    }

    stage('OPA: Apply Constraints') {
      steps {
        sh '''
          kubectl apply -f opa/label-constraint.yaml
          kubectl apply -f opa/probes-constraint.yaml
        '''
      }
    }

  }

  post {
    failure {
      echo 'Build or Deployment Failed. Check logs or trigger rollback manually.'
    }
  }
}
