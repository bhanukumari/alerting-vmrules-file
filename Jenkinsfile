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
                sh '''
                    apt-get update -y
                    apt-get install -y python3 python3-pip
                    pip3 install pyyaml --break-system-packages
                '''
            }
        }
        stage('Convert YAML to JSON') {
            steps {
                sh 'python3 convert.py'
            }
        }
        stage('Push JSON to GitHub') {
            steps {
                sh '''
                    git config user.email "jenkins@opstree.com"
                    git config user.name "Jenkins"
                    git add json_output/
                    git commit -m "Auto: YAML to JSON converted"
                    git push origin main
                '''
            }
        }
    }
}
