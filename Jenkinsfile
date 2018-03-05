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
                sh "docker tag docker-staging.imio.be/iasmartweb/mutual:latest docker-staging.imio.be/iasmartweb/mutual:${env.BUILD_ID}"
                sh "docker push docker-staging.imio.be/iasmartweb/mutual"
                sh "docker rmi docker-staging.imio.be/iasmartweb/mutual"
                sh "docker rmi -f \$(docker images -q docker-staging.imio.be/iasmartweb/mutual)"
            }
        }
        stage('Deploy to staging') {
            when {
              expression {
                currentBuild.result == null || currentBuild.result == 'SUCCESS'
              }
            }
            steps {
                script {
                    deploy.staging 'iasmartweb/mutual'
                }
            }
        }
        stage('Deploy to Prod') {
            input {
                message "Should we deploy to prod ?"
            }
            steps {
                sh '''
                  mco ping
                  # /usr/local/bin/copy_latest_docker_images_to_prod.py
                  # eval $(/usr/local/bin/copy_latest_docker_images_to_prod.py -e)
                  # mco shell run "docker pull docker-prod.imio.be/mutual-website:$latest_tag_id_mutual_website" -C "/role::docker::sites$/" -I /site-prod/
                  # mco shell run 'at -f /srv/docker_scripts/website-update-all-images.sh -t `date -d "tomorrow" +%Y%m%d`0500' -C "/role::docker::sites$/" -I /site-prod/
                '''
            }
        }
    }
}
