@Library('jenkins-pipeline-scripts') _
pipeline {
    agent none
    triggers {
        pollSCM('*/3 * * * *')
    }
    options {
        // Keep the 50 most recent builds
        buildDiscarder(logRotator(numToKeepStr:'50'))
    }
    stages {
       stage('Migrate to 4.3.18.x') {
            agent none
            steps {
                echo "Not use anymore, use branch 4.3.18.x"
            }
        }
    }
}
