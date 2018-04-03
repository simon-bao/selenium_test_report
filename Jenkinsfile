pipeline {
	agent none
	stages {
		stage('编译打包') {
            steps {
                build '0-min-Step-UserUI-Package'
            }
        }
        stage('部署到SVN') {
            steps {
                build '0.min-Step_DeployTo_Tomcat'
            }
        }
		stage('Web测试') {
            steps {
                build 'test-selenium-in-win-Agent'
            }
        }
	}
}