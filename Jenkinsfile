pipeline {
	agent none
	stages {
		stage('代码质量扫描') {
            steps {
                build '2.DTjob-mvn-Package_todo_SonarScanner'
            }
        }
        stage('编译、打包、归档') {
            steps {
                build '3.DTjob-mvn_Build-Tigger-STEP4'
            }
        }
	}
}