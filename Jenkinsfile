#!/usr/bin/env groovy
pipeline {
    agent any
    triggers {
        cron('0 2 * * 0')
    }
    stages {
        stage('Build images') {
            steps {
                sh 'make iasmartweb-build-cache'
            }
        }
    }
    post {
        success {
            sh '''
                docker push docker-staging.imio.be/iasmartweb/cache
                docker rmi $(docker images -q docker-staging.imio.be/iasmartweb/cache)
                docker push docker-staging.imio.be/intranet/cache
                docker rmi $(docker images -q docker-staging.imio.be/intranet/cache)
            '''
        }
    }
}
