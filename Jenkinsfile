@Library('jenkins-pipeline-scripts') _
pipeline {
    agent any
    triggers {
        pollSCM('*/3 * * * *')
    }
    stages {
        stage('Build') {
            steps {
                sh 'make docker-image'
            }
        }
        stage('Push image to registry') {
            steps {
                pushImageToRegistry (
                    "${env.BUILD_ID}",
                    "iasmartweb/mutual"
                )
            }
        }
        stage('Deploy to staging') {
            when {
                expression {
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                deployToStaging (
                    "${currentBuild.result}",
                    "${env.BUILD_ID}",
                    "iasmartweb/mutual",
                    'role::docker::sites$',
                    '/srv/docker_scripts/website-update-all-images.sh'
                )
            }
        }
        stage('Deploy to Prod') {
            input {
                message "Should we deploy to prod ?"
            }
            steps {
                deployToProd (
                    "${env.BUILD_ID}",
                    "iasmartweb/mutual",
                    'role::docker::sites$',
                    '/srv/docker_scripts/website-update-all-images.sh'
                )
            }
        }
    }
}
