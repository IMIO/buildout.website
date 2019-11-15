@Library('jenkins-pipeline-scripts') _
pipeline {
    agent none
    options {
        // Keep the 50 most recent builds
        buildDiscarder(logRotator(numToKeepStr:'50'))
    }
    stages {
        stage('Build') {
            agent any
            steps {
                sh 'make eggs'
                sh 'docker build --pull -t iasmartweb/mutual:alpine .'
            }
        }
        stage('Push image to registry') {
            agent any
            steps {
                sh "docker tag iasmartweb/mutual:alpine docker-staging.imio.be/iasmartweb/mutual:alpine"
                sh "docker tag iasmartweb/mutual:alpine docker-staging.imio.be/iasmartweb/mutual:alpine-$BUILD_ID"
                sh "docker push docker-staging.imio.be/iasmartweb/mutual:alpine"
                sh "docker push docker-staging.imio.be/iasmartweb/mutual:alpine-$BUILD_ID"
            }
        }
        stage('Deploy to staging') {
            agent any
            when {
                expression {
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                sh "mco shell run 'docker pull docker-staging.imio.be/iasmartweb/mutual:alpine-$BUILD_ID' -I /^staging.imio.be/"
                echo "mco shell run '/srv/docker_scripts/website-update-all-images.sh' -t 1200 --tail -I /^staging.imio.be/"
            }
        }
        stage('Deploy to prod ?') {
            agent none
            steps {
                timeout(time: 24, unit: 'HOURS') {
                    input (
                        message: 'Should we deploy to prod ?'
                    )
                }
            }
            post {
                aborted {
                    echo 'In post aborted'
                }
                success {
                    echo 'In post success'
                }
            }
        }
        stage('Deploying to prod') {
            agent any
            steps {
                echo "To be done !"
            }

        }
    }
}
