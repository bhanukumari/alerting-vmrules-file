pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/bhanukumari/alerting-vmrules-file.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install pyyaml --break-system-packages || pip install pyyaml --break-system-packages'
            }
        }

        stage('Convert YAML to JSON') {
            steps {
                sh 'python3 convert.py'
            }
        }
    }
}