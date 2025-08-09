pipeline {
  agent any

  environment {
    IMAGE_NAME = "self-healing-app"
    DOCKER_REGISTRY = "ppankajs"
    TAG = "v${BUILD_NUMBER}"
  }

  stages {

    stage('Clone Repo') {
      steps {
        git credentialsId: 'github-credentials', url: 'https://github.com/ppankajs/app.git'
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
          docker.withRegistry('', 'docker-credentials') {
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
          sed 's|ppankajs/self-healing-app:latest|${DOCKER_REGISTRY}/${IMAGE_NAME}:${TAG}|' k8s/deployment.yaml | kubectl apply -f -
        """
      }
    }

    stage('Expose Flask Service') {
      steps {
        sh 'kubectl apply -f k8s/service.yaml'
        // sh 'kubectl apply -f k8s/prometheus-additional-scrape-config.yaml'
      }
    }

    stage('RBAC for Trust Check CronJob') {
      steps {
        sh 'kubectl apply -f k8s/trust-score-rbac.yaml'
	      sh 'kubectl apply -f k8s/failure-sa.yaml'
	      sh 'kubectl apply -f k8s/rollback-access.yaml'
	      sh 'kubectl apply -f k8s/rollback-access.yaml'
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
              sed 's|ppankajs/self-healing-app:latest|${DOCKER_REGISTRY}/${IMAGE_NAME}:${TAG}|' k8s/cronjobs/${cron} | kubectl apply -f -
            """
          }
        }
      }
    }

    stage('OPA: Apply Constraint Templates') {
      steps {
        sh '''
          # Delete template if exists
          kubectl delete constrainttemplate k8srequiredprobes --ignore-not-found

          # Apply templates
          kubectl apply -f opa/templates/label-template.yaml
          kubectl apply -f opa/templates/probes-template.yaml

          echo "Waiting for CRD 'k8srequiredprobes.constraints.gatekeeper.sh' to be registered and usable..."

          # Wait loop for CRD to become available
          for i in {1..12}; do
            echo "Attempt $i: Checking if CRD exists and is ready..."
            kubectl get crd k8srequiredprobes.constraints.gatekeeper.sh >/dev/null 2>&1 && break
            sleep 5
          done

          # Final confirmation (with fail-safe)
          if ! kubectl get crd k8srequiredprobes.constraints.gatekeeper.sh >/dev/null 2>&1; then
            echo "CRD k8srequiredprobes.constraints.gatekeeper.sh' not found after waiting. Aborting."
            exit 1
          fi

          echo "CRD is ready!"
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
