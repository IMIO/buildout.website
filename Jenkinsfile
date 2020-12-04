@Library('jenkins-pipeline-scripts') _

pipeline {
  agent none
  options {
    buildDiscarder(logRotator(numToKeepStr:'50'))
  }
  stages {
    stage('Build') {
      agent any
      when {
        allOf{
          branch "main"
          not {
            changelog '.*\\[(ci)?\\-?\\s?skip\\-?\\s?(ci)?\\].*'
          }
          not {
            changelog '^Back to development:*'
          }
          not {
            changelog '^Preparing release *'
          }
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
        allOf{
          branch "main"
          not {
            changelog '.*\\[(ci)?\\-?\\s?skip\\-?\\s?(ci)?\\].*'
          }
          not {
            changelog '^Back to development:*'
          }
          not {
            changelog '^Preparing release *'
          }
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
          expression {
            currentBuild.result == null || currentBuild.result == 'SUCCESS'
          }
          not {
            changelog '.*\\[(ci)?\\-?\\s?skip\\-?\\s?(ci)?\\].*'
          }
          not {
            changelog '^Back to development:*'
          }
          not {
            changelog '^Preparing release *'
          }
        }
      }
      steps {
        sh "mco shell run 'docker pull docker-staging.imio.be/iasmartweb/mutual:$BUILD_ID' -I /^site-staging/ -I /^staging.imio.be/"
        sh "mco shell run '/srv/docker_scripts/website-update-all-images.sh' -t 1200 --tail -I /^site-staging/ -I /^staging.imio.be/"
      }
    }
    stage('Deploy') {
      agent any
      when {
        buildingTag()
      }
      steps {
        echo 'Deploying only because this commit is tagged...'
        echo "Branch: $BRANCH_NAME"
        echo "Tag: $TAG_NAME"
        moveImageToProdRegistry(env.TAG_NAME, "iasmartweb/mutual")
        echo "Schedule Rundeck job"
        sh 'curl -XPOST -H "x-Rundeck-Auth-Token:$RUNDECK_TOKEN" -F "runAtTime=`date --date=\"05:00 tomorrow\" +\"%Y-%m-%dT%H:%M:%S%z\"`" -F "option.tag=$TAG_NAME" https://run.imio.be/api/24/job/194bda58-e3d5-4fbe-81d7-3e9fbfd8ebad/run'
        mail to: 'support-web@imio.be',
          subject: "New release will be deploy tomorrow: ${currentBuild.displayName}",
          body: "The pipeline ${env.JOB_NAME} ${env.BUILD_NUMBER} released ${env.fullDisplayName} <br />See <a href='https://github.com/IMIO/buildout.website/blob/main/CHANGES.rst'>Changelog</a><br />Upgrade will start tomorrow at 5am."
        echo 'Upgrade finished.'
      }
    }
    stage('Deploy now') {
      agent any
      when {
        tag ".*bugfix.*"
      }
      steps {
        echo 'Deploying now'
        echo "Tag: $TAG_NAME"
        echo "Schedule Rundeck job"
        sh 'curl -XPOST -H "x-Rundeck-Auth-Token:$RUNDECK_TOKEN" -F "option.tag=$TAG_NAME" https://run.imio.be/api/24/job/609802e6-2631-43d2-908f-88822c0f5ea6/run'
        mail to: 'support-web@imio.be',
          subject: "New release is deploying now: ${currentBuild.displayName}",
          body: "The pipeline ${env.JOB_NAME} ${env.BUILD_NUMBER} finished and a new release is starting to update now ${env.fullDisplayName} <br />See <a href='https://github.com/IMIO/buildout.website/blob/main/CHANGES.rst'>Changelog</a>"
        echo 'Upgrade finished.'
      }
    }
  }
  post {
    always {
      node(null)  {
        sh "rm -rf eggs/"
      }
    }
  }
}
