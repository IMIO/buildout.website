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
            pushImageToRegistry {
                buildId = "${env.BUILD_ID}"
                imageName = "iasmartweb/mutual"
            }
        }
        stage('Deploy to staging') {
            deployToStaging {
                currentBuildResult = "${currentBuild.result}"
                buildId = "${env.BUILD_ID}"
                imageName = "iasmartweb/mutual"
                role = 'role::docker::sites$'
                updateScript = '/srv/docker_scripts/website-update-all-images.sh'
            }
        }
        stage('Deploy to Prod') {
            deployToProd {
                buildId = "${env.BUILD_ID}"
                imageName = "iasmartweb/mutual"
                role = 'role::docker::sites$'
                updateScript = '/srv/docker_scripts/website-update-all-images.sh'
            }
        }
    }
}
