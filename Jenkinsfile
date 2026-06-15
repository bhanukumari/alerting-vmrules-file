pipeline {
    agent any

    triggers {
        githubPush()
    }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/bhanukumari/alerting-vmrules-file.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'python3 -m pip install pyyaml --user'
            }
        }

        stage('Convert YAML to JSON') {
            steps {
                sh 'python3 convert.py'
            }
        }
    }

}


