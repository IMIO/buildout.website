#!/usr/bin/env groovy
pipeline {
    agent any
    triggers {
        cron('30 2 * * 0')
    }
    stages {
        stage('Build image') {
            steps {
                sh 'make docker-build-cache'
            }
        }
    }
    post {
        success {
            sh '''
                docker push docker-staging.imio.be/iasmartweb/cache
		docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
                docker rmi $(docker images -q docker-staging.imio.be/iasmartweb/cache)
            '''
        }
    }
}
