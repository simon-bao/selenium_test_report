pipeline {
  agent none
  stages {
    stage('Group1') {
      parallel {
        stage('stage1') {
          steps {
            build '0-min-Step-UserUI-Package'
            build 'test-selenium-in-win-Agent'
          }
        }
        stage('stage2') {
          steps {
            build 'test-selenium-in-win-Agent'
          }
        }
      }
    }
    stage('stage2') {
      steps {
        build '0.min-Step_DeployTo_Tomcat'
      }
    }
    stage('stage3') {
      steps {
        build 'test-selenium-in-win-Agent'
      }
    }
  }
  environment {
    Build_User = 'Bob'
    Usage = 'test BO'
  }
}