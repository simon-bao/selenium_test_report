pipeline {
	agent none
	stages {
		stage('代码质量扫描') {
            steps {
                build '0.min-Step_Compile'
            }
        }
        stage('编译、打包、归档') {
            steps {
                build '0.AdminUI_V1.0_Test2_package'
            }
        }
	}
}