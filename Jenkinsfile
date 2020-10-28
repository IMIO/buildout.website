@Library('jenkins-pipeline-scripts') _

pipeline {
    agent none
    options {
        // Keep the 50 most recent builds
        buildDiscarder(logRotator(numToKeepStr:'50'))
    }
    stages {
        stage('Initialize'){
            steps {
                script {
                    checkout scm
                    SKIP_PATTERN = ".*?(ci.)?skip(.ci)?.*"
                    SKIP = false
                    commitMessage = sh(script: "git log --oneline -1", returnStdout: true)
                    commitMessage = commitMessage.trim()
                    commitMessage = commitMessage.toLowerCase()
                    echo "commitMessage = '${commitMessage}'"
                    SKIP = BRANCH_NAME == "main" && commitMessage ==~ SKIP_PATTERN
                    echo "SKIP = ${SKIP}"
                    if (SKIP == true) {
                        currentBuild.result = 'NOT_BUILT'
                    }
                }
            }
        }
        stage('Build') {
            agent any
            when {
                allOf {
                    expression {SKIP == false}
                    branch "main"
                }
            }
            steps {
                sh 'make eggs'
                sh 'make docker-image'
            }
        }
        stage('Push image to staging registry') {
            agent any
                when {
                allOf {
                    expression {SKIP == false}
                    branch "main"
                }
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
                    expression {SKIP == false}
                    expression {
                        currentBuild.result == null || currentBuild.result == 'SUCCESS'
                    }
                }
            }
            steps {
                sh "mco shell run 'docker pull docker-staging.imio.be/iasmartweb/mutual:$BUILD_ID' -I /^site-staging/ -I /^staging.imio.be/"
                sh "mco shell run '/srv/docker_scripts/website-update-all-images.sh' -t 1200 --tail -I /^site-staging/ -I /^staging.imio.be/ "
            }
        }
        stage('Deploy') {
            when { tag "release-*" }
            steps {
                echo 'Deploying only because this commit is tagged...'
                echo "Branch: $BRANCH_NAME"
                echo "Tag: $TAG_NAME"
                moveImageToProdRegistry(
                    $TAG_NAME,
                    "iasmartweb/mutual"
                )
                echo 'You have to start rundeck job now.'
            }
        }
    }
}
