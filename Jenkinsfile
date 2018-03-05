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
                pushImageToRegistry {
                    buildId = "${env.BUILD_ID}"
                    imageName = "iasmartweb/mutual"
                }
            }
        }
        stage('Deploy to staging') {
            when {
                expression {
                    currentBuildResult == null || currentBuildResult == 'SUCCESS'
                }
            }
            steps {
                deployToStaging {
                    currentBuildResult = "${currentBuild.result}"
                    buildId = "${env.BUILD_ID}"
                    imageName = "iasmartweb/mutual"
                    role = 'role::docker::sites$'
                    updateScript = '/srv/docker_scripts/website-update-all-images.sh'
                }
            }
        }
        stage('Deploy to Prod') {
            input {
                message "Should we deploy to prod ?"
            }
            steps {
                deployToProd {
                    buildId = "${env.BUILD_ID}"
                    imageName = "iasmartweb/mutual"
                    role = 'role::docker::sites$'
                    updateScript = '/srv/docker_scripts/website-update-all-images.sh'
                }

        }
    }
}
