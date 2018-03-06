@Library('jenkins-pipeline-scripts') _

iasmartwebDeliveryPipeline(
    buildId: "${env.BUILD_ID}",
    imageName: "iasmartweb/mutual",
    role: 'role::docker::sites$',
    updateScript: '/srv/docker_scripts/website-update-all-images.sh'
)
