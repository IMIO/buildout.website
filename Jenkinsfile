@Library('jenkins-pipeline-scripts') _
pipeline {
    agent any
    triggers {
        pollSCM('*/3 * * * *')
    }
    environment {
        yyyymmdd = Generic.tagtime()
    }
    stages {
        stage('Build') {
            steps {
                sh 'make docker-image'
            }
        }
        stage('Push image to registry') {
            steps {
                sh '''
                  docker tag docker-staging.imio.be/iasmartweb/mutual:latest  docker-staging.imio.be/iasmartweb/mutual:$yyyymmdd-${env.BUILD_ID}
                  docker push docker-staging.imio.be/iasmartweb/mutual
                  docker rmi $(docker images -q docker-staging.imio.be/iasmartweb/mutual)
                '''
            }
        }
        stage('Deploy to staging') {
            when {
              expression {
                currentBuild.result == null || currentBuild.result == 'SUCCESS'
              }
            }
            steps {
                sh '''
                  mco shell run "docker pull docker-staging.imio.be/iasmartweb/mutual:$yyyymmdd-${env.BUILD_ID}" -C "/role::docker::sites$/" -I /staging.imio.be/
                  mco shell run -t 1200 -C "/role::docker::sites$/" -I "/staging.imio.be/" --tail 'bash -c "PATH=/usr/local/bin:/opt/puppetlabs/bin:$PATH /srv/docker_scripts/website-update-all-images.sh"'
                '''
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
