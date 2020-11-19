@Library('jenkins-pipeline-scripts') _

pipeline {
    agent none
    options {
        // Keep the 50 most recent builds
        buildDiscarder(logRotator(numToKeepStr:'50'))
    }
    stages {
        stage('Code fetching') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            agent any
            when {
                branch "main"
            }
            steps {
                sh 'make eggs'
                sh 'make docker-image'
            }
        }
        stage('Push image to staging registry') {
            agent any
            when {
                branch "main"
            }
            steps {
                echo '''
                  pushImageToRegistry (
                    env.BUILD_ID,
                    "iasmartweb/mutual"
                  )
                '''
            }
        }
        stage('Deploy to staging') {
            agent any
            when {
                allOf {
                    branch "main"
                    expression {
                        currentBuild.result == null || currentBuild.result == 'SUCCESS'
                    }
                }
            }
            steps {
                echo "mco shell run 'docker pull docker-staging.imio.be/iasmartweb/mutual:$BUILD_ID' -I /^site-staging/ -I /^staging.imio.be/"
                echo "mco shell run '/srv/docker_scripts/website-update-all-images.sh' -t 1200 --tail -I /^site-staging/ -I /^staging.imio.be/ "
            }
        }
        stage('Deploy') {
            when {
                buildingTag()
            }
            steps {
                echo 'Deploying only because this commit is tagged...'
                echo "Branch: $BRANCH_NAME"
                echo "Tag: $TAG_NAME"
                echo 'moveImageToProdRegistry($TAG_NAME, "iasmartweb/mutual")'
                echo 'curl --fail -XPOST --header "Content-Type:application/json" --header "X-Rundeck-Auth-Token:$RUNDECK_TOKEN" https://run.imio.be/api/14/job/dfc15fd1-e07f-43e8-aea2-e34a97cfc65c/run'
                echo 'You have to start rundeck job now.'
            }
        }
    }
}
