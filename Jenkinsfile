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
                pushImageToRegistry (
                    env.BUILD_ID,
                    "iasmartweb/mutual"
                )
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
                sh "mco shell run 'docker pull docker-staging.imio.be/iasmartweb/mutual:$BUILD_ID' -I /^site-staging/ -I /^staging.imio.be/"
                sh "mco shell run '/srv/docker_scripts/website-update-all-images.sh' -t 1200 --tail -I /^site-staging/ -I /^staging.imio.be/"
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
                moveImageToProdRegistry($TAG_NAME, "iasmartweb/mutual")
                sh 'curl --fail -XPOST -H "Content-Type:application/json" -H "X-Rundeck-Auth-Token:$RUNDECK_TOKEN" -H "runAtTime:`date --date=\"05:00 tomorrow\" -Iseconds`" https://run.imio.be/api/14/job/194bda58-e3d5-4fbe-81d7-3e9fbfd8ebad/run'
                echo 'You have to start rundeck job now.'
            }
        }
    }
}
