pipeline {
  agent any

  environment {
    AWS_ACCOUNT_ID = '277385995709'
    AWS_REGION     = 'us-east-1'
    CLUSTER_NAME   = 'streamingapp-cluster'
    SNS_SUCCESS_TOPIC = "arn:aws:sns:us-east-1:277385995709:streamingapp-deploy-success"
    SNS_FAILURE_TOPIC = "arn:aws:sns:us-east-1:277385995709:streamingapp-deploy-failure"
  }

  stages {
    stage('Checkout') {
      steps {
        script { env.LAST_STAGE = 'Checkout' }
        checkout scm
      }
    }

    stage('Configure kubeconfig') {
      steps {
        script { env.LAST_STAGE = 'Configure kubeconfig' }
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'streamingapp-tanishq-aws-creds']]) {
          sh "aws eks update-kubeconfig --name ${CLUSTER_NAME} --region ${AWS_REGION}"
        }
      }
    }

    stage('Helm upgrade') {
      steps {
        script { env.LAST_STAGE = 'Helm upgrade' }
        withCredentials([
          [$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'streamingapp-tanishq-aws-creds'],
          file(credentialsId: 'streamingapp-tanishq-values-secret', variable: 'SECRET_VALUES_FILE')
        ]) {
          sh """
            helm upgrade --install streamingapp ./helm/streamingapp \
              -f helm/streamingapp/values.yaml \
              -f \$SECRET_VALUES_FILE \
              --wait --timeout 5m
          """
        }
      }
    }

    stage('Verify rollout') {
      steps {
        script { env.LAST_STAGE = 'Verify rollout' }
        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'streamingapp-tanishq-aws-creds']]) {
          sh '''
            kubectl rollout status deploy/auth --timeout=120s
            kubectl rollout status deploy/streaming --timeout=120s
            kubectl rollout status deploy/admin --timeout=120s
            kubectl rollout status deploy/chat --timeout=120s
            kubectl rollout status deploy/frontend --timeout=120s
          '''
        }
      }
    }
  }

  post {
    success {
      echo "Deploy SUCCESS — commit ${env.GIT_COMMIT}"
      withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'streamingapp-tanishq-aws-creds']]) {
        sh """
          aws sns publish --region ${AWS_REGION} --topic-arn ${SNS_SUCCESS_TOPIC} \
            --subject "StreamingApp deploy succeeded" \
            --message "Commit ${env.GIT_COMMIT} deployed successfully to ${CLUSTER_NAME}. Build: ${env.BUILD_URL}" \
            || true
        """
      }
    }
    failure {
      echo "Deploy FAILED at stage [${env.LAST_STAGE ?: 'Checkout'}] — commit ${env.GIT_COMMIT}"
      withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'streamingapp-tanishq-aws-creds']]) {
        sh """
          aws sns publish --region ${AWS_REGION} --topic-arn ${SNS_FAILURE_TOPIC} \
            --subject "StreamingApp deploy FAILED" \
            --message "Commit ${env.GIT_COMMIT} failed at stage [${env.LAST_STAGE ?: 'Checkout'}] on ${CLUSTER_NAME}. Build: ${env.BUILD_URL}" \
            || true
        """
      }
    }
  }
}
